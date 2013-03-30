# -*- coding: utf-8 -*-

# stdlib
import time
import collections

# 3rd party
import webob
import webapp2

# gevent
import gevent
from gevent import pool
from gevent import queue

# hermes codebase
import event
import protocol
import datastore
import components

# hermes config
import config
from config import debug
from config import verbose
from config import _BLOCK_PDB
from config import _HEADER_PREFIX
from config import _REDIS_WRITE_POOL
from config import _PREBUFFER_FREQUENCY
from config import _PREBUFFER_THRESHOLD

# hermes util
import util
from util import exceptions

# application components
from event import AllParams
from event import AmpushParams
from event import InternalParams


# Globals
_TRACKER_VERSION = (0, 1)  # advertised in `AMP-Tracker` response header
_TRACKER_RELEASE = "alpha"  # advertised in `AMP-Tracker` response header
_TRACKER_MODE = protocol.TrackerMode.DEBUG  # advertised in `AMP-Mode` response header


## EventTracker - server that tracks events, triggered via special URLs
class EventTracker(object):

    ''' WSGI-compliant application that tracks URL-dispatched events. '''

    # Base HTTP Template
    request_class = webob.Request
    response_class = webob.Response
    content_type = ('text/html', 'utf-8')
    _base_headers = {

        ('%s-Mode' % _HEADER_PREFIX): protocol.TrackerMode.DEBUG,
        ('%s-Tracker' % _HEADER_PREFIX): '-'.join(('.'.join(map(str, _TRACKER_VERSION)), _TRACKER_RELEASE))

    }.items()

    # Object Params
    past = None  # the immediately-past buffer
    debug = debug  # whether the tracker runs in debug mode
    active = None  # the currently-active buffer
    params = None  # parameterset passed via the URL
    engine = None  # datastore execution engine
    chunked = True  # indicate server-side support for chunked encoding
    session = None  # existing session cookie, if any
    lastflush = None  # holds a timestamp with the last flush
    flushqueue = None  # holds queued redis write greenlets
    staged_flush = False  # stage to flush the superbuffer
    log_prefix = "TRACKER"  # prefix all log messages from this tracker with X
    header_prefix = _HEADER_PREFIX  # prefix all HTTP response headers with X

    # Engine / Event Classes
    event_class = event.TrackedEvent  # class to use as tracked event objects
    engine_class = datastore.DatastoreEngine  # class to use as delegated data controller

    # Buffers
    prebuffer = pool.Group()  # prebuffer execution queue
    framebuffer = collections.deque()  # holds full frames for datastore engine


    # Buffer Configuration
    class BufferConfig(object):

        ''' Static config class for `EventTracker`. '''

        frequency = _PREBUFFER_FREQUENCY  # empty the buffer every X seconds...
        threshold = _PREBUFFER_THRESHOLD  # ...or every Y events, whichever comes first

    def __init__(self, platform='WSGI', event=None, engine=None):

        ''' Initialize this `EventTracker`. '''

        # Default `lastflush` to now...
        self.lastflush = int(time.time())
        self.engine = engine() if engine else self.engine_class(self)

        if debug:
            self.log("Debug mode is %s, serving on port %s." % ("ON" if self.debug else "OFF", config._DEBUG_PORT))

        # Allow overwriting the TrackedEvent implementation class
        if event:
            self.event_class = event

    def _output(self, message, prefix=None):

        ''' Low-level output pipe. '''

        if prefix:
            print "[%s] %s: %s" % (self.log_prefix, prefix, message)
        else:
            print "[%s]: %s" % (self.log_prefix, message)
        return self

    @webapp2.cached_property
    def verbose(self):

        ''' Log something only if we're in debug AND verbose mode. '''

        if not (self.debug and verbose):
            def _verbose_blackhole(message):

                ''' Drop invokee data if verbose & debug aren't enabled. '''

                return
            return _verbose_blackhole
        else:
            def _log_verbose(message):

                '''  Invoke log output function. '''

                return self._output(message)
            return _log_verbose

    @webapp2.cached_property
    def log(self):

        ''' Log something if we're in debug mode. '''

        if not self.debug:
            def _log_blackhole(message):

                ''' Drop invokee data if debug isn't enabled. '''

                return
            return _log_blackhole
        else:
            def _log_debug(message):

                ''' Invoke log output function. '''

                return self._output(message)
            return _log_debug

    def warn(self, message):

        ''' Log a warning. '''

        self._output(message, "WARN")
        return self

    def error(self, message):

        ''' Log an error. '''

        self._output(message, "ERROR")
        return self

    def buffer(self, event):

        ''' Add a `TrackedEvent` to the in-memory buffer. '''

        if debug:
            self.log("Sending event %s to prebuffer." % event.id)
            self.log("Current prebuffer length: %s." % len(self.prebuffer))

        self.prebuffer.add(event)

        # See if the buffer needs to be flushed
        should_flush = self.check()
        if should_flush:
            self.flush()

        return event.id, should_flush

    def check(self):

        ''' See if we need to close out the prebuffer. '''

        # We should flush if we've A) overflowed our soft buffer threshold or B) passed our flush timeout...
        timestamp = int(time.time())
        flush = ((len(self.prebuffer) > self.BufferConfig.threshold) or (self.lastflush + self.BufferConfig.frequency < timestamp))
        
        # Send logs
        did_timeout = "IS" if (self.lastflush + self.BufferConfig.frequency < timestamp) else "IS NOT"

        if debug:
            self.verbose("Current timestamp: %s." % timestamp)
            self.log("Buffer: Checkin-in at size %s with lastflush %s, which %s more than interval %s." % (len(self.prebuffer), self.lastflush, did_timeout, self.BufferConfig.frequency))
            self.log("Flush %s recommended." % ("IS" if flush else "IS NOT"))
        
        return flush

    def flush(self):

        ''' Flush the prebuffer batch to the frame buffer. '''

        # Take new timestamp, log what we're doing...
        timestamp = int(time.time())
        if debug:
            self.log("Buffer: Flushing buffer %s of %s events, resetting timestamp to %s." % (id(self.prebuffer), len(self.prebuffer), timestamp))

        # Grab current prebuffer, allocate next prebuffer...
        current_prebuffer = self.prebuffer
        next_prebuffer = pool.Group()

        # Buffer the current frame in the framebuffer...
        self.framebuffer.append(current_prebuffer)

        # Replace current buffer with new one.
        if debug:
            self.log("Buffer: provisioned new prebuffer batch group at ID \"%s\"." % id(next_prebuffer))
        self.prebuffer = next_prebuffer

        self.lastflush = timestamp

        if len(self.framebuffer) > 1:
            if debug:
                self.log("Buffer: Framebuffer ready to push writes. Superflush IS recommended.")
            self.staged_flush = True

        return self

    def superflush(self):

        ''' Flush the frame buffer to the DatastoreEngine. '''

        if debug:
            self.log("Buffer: Flushing framebuffer to DatastoreEngine.")
            self.log("Buffer: Switched active frame to buffer ID %s." % id(self.active))

        # Copy over immediate-past-frame
        if self.active:
            self.past = self.active

        self.active = self.framebuffer.popleft()

        # There's a flush staged for the DatastoreEngine...
        self.engine.inbox.put_nowait(self.active)

        return self

    def begin_request(self, environ, start_response):

        ''' Factory a new `webob.Request`/`webob.Response` pair, representing a new HTTP transaction cycle. '''

        # Spawn request + response
        content_type, encoding = self.content_type
        request, response = self.request_class(environ), self.response_class(content_type=content_type, charset=encoding)

        if verbose:
            self.verbose("=========== Request Environment ===========")
            self.verbose(str(environ))
            self.verbose("Provisioned WSGI request/response pair with IDs (%s, %s)." % (id(request), id(response)))
            self.verbose("Original response headers: \"%s\"." % response.headers)

            # Fill-in response info
            response.stage = protocol.ResponseStage.PENDING
            response.request = request
            for hkey, hvalue in self._base_headers:
                response.headers[hkey] = hvalue

        if self.chunked:

            # Remove Content-Length for a chunked response
            self.verbose('Running in CHUNKED mode, removing Content-Length header.')
            del response.headers['Content-Length']

        if verbose:
            self.verbose("Updated response headers: \"%s\"." % response.headers)
        return request, response

    def send_response(self, response, start_response, flush=False):

        ''' Send the WSGI start_response call, optionally flushing the response buffer and finishing the transaction. '''

        if response.stage == protocol.ResponseStage.PENDING:

            # Send log messages
            if verbose:
                self.verbose("Beginning response transmission.")
                self.verbose("Sending %s response with status \"%s\" and %s headers." % ("immediate" if flush else "deferred", response.status, len(response.headerlist)))
                self.verbose("Full response headers: \"%s\"." % response.headerlist)

            # Start response            
            start_response(response.status, response.headerlist)
            response.stage = protocol.ResponseStage.STARTED
            return response.status, response.headerlist

        elif response.stage == protocol.ResponseStage.STARTED:

            # We've already started the response.
            self.verbose("Response already started, resuming deferred transaction.")

            return response.body

        if flush:

            if verbose:
                self.verbose("Flushing response body of length %s." % len(response.body))
                self.verbose("Full response body: \"%s\"." % response.app_iter)
            return response.body

        else:
            return response

    def __call__(self, environ, start_response):

        ''' Handle a hit to a tracker URL. '''

        if debug and verbose and _BLOCK_PDB:
            import pdb; pdb.set_trace()

        # Spawn request + response
        response_buffer = []
        request, response = self.begin_request(environ, start_response)
        self.log("Processing new request with ID %s." % id(request))

        try:
            # Factory new `TrackedEvent`.
            event = self.event_class.new(self, request, response)
            self.log("Spawned new `TrackedEvent` with ID %s." % event.id)

            # Begin building headers.
            response.headers['%s-Match' % self.header_prefix] = event.match
            response.headers['%s-Session' % self.header_prefix] = event.session

            self.log("Encountered match value %s with session %s." % (event.match, event.session))

        except exceptions.ClientError as e:

            # Handle 400-bound ClientError(s)
            response.status = 400
            self.error("Encountered ClientError: \"%s\". Raising HTTP400." % e)

            body = self.send_response(response, start_response, flush=True)
            yield body
            raise StopIteration()

        except exceptions.PlatformError as e:

            # Handle 500-bound PlatformError(s)
            response.status = 500
            self.error("Encountered PlatformError: \"%s\". Raising HTTP500." % e)

            body = self.send_response(response, start_response, flush=True)
            yield body
            raise StopIteration()

        except exceptions.Error as e:

            # Handle 500-bound critical errors.
            self.error("Encountered known (but unhandled) exception: \"%s\"." % e)
            self.error("Exception description: \"%s\"." % e.__doc__)

            response.status = 500
            body = self.send_response(response, start_response, flush=True)
            yield body
            raise  # re-raise after response
            raise StopIteration()

        self.verbose("Successfully provisioned new TrackedEvent. Starting deferred response.")

        # Start response with appropriate headers
        self.send_response(response, start_response, flush=False)

        # Buffer it and grab a simple ID to display
        self.verbose("Buffering event to write prebuffer.")
        buffer_id, flushed = self.buffer(event)
            
        # Yield status message if debug mode is enabled.
        response_buffer.append(u"TrackedEvent submitted with ID %s." % buffer_id)
        if flushed:
            response_buffer.append("<b>Flushed buffer with ID %s.</b><br />" % None)
        response_buffer.append(u"<b>Prebuffer:</b> ID \"%s\" of size: %s" % (id(self.prebuffer), len(self.prebuffer)))

        # We're done processing. Flush buffer and respond.
        self.log("Tracker transaction completed. Writing body.")
        self.verbose("Tracker response buffer of length %s:" % len(response_buffer))
        self.verbose(str(response_buffer))
        response.text = u"\n".join(response_buffer)

        response.stage = protocol.ResponseStage.COMPLETE
        self.verbose('Yielding to server-side transport.')
        for chunk in response.app_iter:
            yield chunk

        # Perform staged flush, if any...
        if self.staged_flush:
            self.staged_flush = False
            gevent.spawn(self.superflush)
            gevent.sleep(0)

        raise StopIteration()
