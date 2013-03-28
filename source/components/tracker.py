# -*- coding: utf-8 -*-

# stdlib
import time

# 3rd party
import webob

# gevent
import gevent
from gevent import queue

# hermes codebase
from apps.hermes.source import debug
from apps.hermes.source import verbose
from apps.hermes.source import protocol
from apps.hermes.source import exceptions
from apps.hermes.source import components
from apps.hermes.source import _BLOCK_PDB
from apps.hermes.source import _REDIS_WRITE_POOL

# application components
from apps.hermes.source.components.event import AllParams
from apps.hermes.source.components.event import TrackedEvent
from apps.hermes.source.components.event import AmpushParams
from apps.hermes.source.components.event import InternalParams
from apps.hermes.source.components.datastore import DatastoreEngine


# Globals
_prebuffer = queue.Queue()  # prebuffer execution queue
_TRACKER_VERSION = (0, 1)   # advertised in `AMP-Tracker` response header
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

        'AMP-Mode': protocol.TrackerMode.DEBUG,
        'AMP-Tracker': '-'.join(('.'.join(map(str, _TRACKER_VERSION)), _TRACKER_RELEASE))

    }.items()

    # Object Params
    params = None  # parameterset passed via the URL
    chunked = True  # indicate server-side support for chunked encoding
    session = None  # existing session cookie, if any
    prebuffer = None  # buffers according to the limits above
    lastflush = None  # holds a timestamp with the last flush
    flushqueue = None  # holds queued redis write greenlets
    log_prefix = "TRACKER"  # prefix all log messages from this tracker with X

    # Engine / Event Classes
    event_class = TrackedEvent  # class to use as tracked event objects
    engine_class = DatastoreEngine  # class to use as delegated data controller

    # Buffer Configuration
    class BufferConfig(object):

        ''' Static config class for `EventTracker`. '''

        frequency = 30  # empty the buffer every X seconds...
        threshold = 100  # ...or every Y events, whichever comes first

    def __init__(self, platform='WSGI'):

        ''' Initialize this `EventTracker`. '''

        # Default `lastflush` to now...
        self.lastflush = int(time.time())
        self.log("Debug mode is %s." % ("ON" if self.debug else "OFF"))
        self.log("Allocated writepool of size %s." % _REDIS_WRITE_POOL)

    @property
    def debug(self):

        ''' Indicate whether we're in debug mode. '''

        return debug

    @property
    def prebuffer(self):

        ''' Grab the global prebuffer. '''

        global _prebuffer
        return _prebuffer

    def _output(self, message, prefix=None):

        ''' Low-level output pipe. '''

        if prefix:
            print "[%s] %s: %s" % (self.log_prefix, prefix, message)
        else:
            print "[%s]: %s" % (self.log_prefix, message)
        return self

    def log(self, message):

        ''' Log something if we're in debug mode. '''

        if self.debug:
            self._output(message)
        return self

    def warn(self, message):

        ''' Log a warning. '''

        self._output(message, "WARN")
        return self

    def error(self, message):

        ''' Log an error. '''

        self._output(message, "ERROR")
        return self

    def verbose(self, message):

        ''' Log something only if we're in debug AND verbose mode. '''

        if self.debug and verbose:
            self._output(message)
        return self

    def buffer(self, event):

        ''' Add a `TrackedEvent` to the in-memory buffer. '''

        self.log("Sending event %s to prebuffer." % event.id)
        self.prebuffer.put_nowait(event)

        # See if the buffer needs to be flushed
        self.verbose("Checking buffer.")
        should_flush = self.check
        if should_flush:
            self.flush()

        return event.id, should_flush

    def check(self):

        ''' See if we need to close out the prebuffer. '''

        # We should flush if we've A) overflowed our soft buffer threshold or B) passed our flush timeout...
        timestamp = int(time.time())
        flush = ((self.prebuffer.qsize() > self.BufferConfig.threshold) or (self.lastflush + self.BufferConfig.frequency < timestamp))
        
        # Send logs
        did_timeout = "IS" if (self.lastflush + self.BufferConfig.frequency < timestamp) else "IS NOT"
        self.verbose("Current timestamp: %s." % timestamp)
        self.log("Buffer: Checkin-in at size %s with lastflush %s, which %s more than interval %s." % (self.prebuffer.qsize(), self.lastflush, did_timeout, self.BufferConfig.frequency))
        self.log("Flush %s recommended." % ("IS" if flush else "IS NOT"))
        
        return flush

    def flush(self):

        ''' Flush the prebuffer to Redis. '''

        timestamp = int(time.time())
        self.log("Buffer: Flushing %s events, resetting timestamp to %s." % (self.prebuffer.qsize(), timestamp))
        self.lastflush = timestamp
        return self

    def begin_request(self, environ, start_response):

        ''' Factory a new `webob.Request`/`webob.Response` pair, representing a new HTTP transaction cycle. '''

        # Spawn request + response
        content_type, encoding = self.content_type
        request, response = self.request_class(environ), self.response_class(content_type=content_type, charset=encoding)

        if verbose:
            self.verbose("===== Request Environment =====")
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

        self.verbose("Updated response headers: \"%s\"." % response.headers)
        return request, response

    def send_response(self, response, start_response, flush=False):

        ''' Send the WSGI start_response call, optionally flushing the response buffer and finishing the transaction. '''

        self.verbose("Beginning response transmission.")
        if response.stage == protocol.ResponseStage.PENDING:
            # Send log messages
            self.log("Sending %s response with status \"%s\" and %s headers." % ("immediate" if flush else "deferred", response.status, len(response.headerlist)))
            self.verbose("Full response headers: \"%s\"." % response.headerlist)

            # Start response            
            start_response(response.status, response.headerlist)
            response.stage = protocol.ResponseStage.STARTED

        elif response.stage == protocol.ResponseStage.STARTED:
            # We've already started the response.
            self.log("Response already started, resuming deferred transaction.")

        if flush:
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
            response.headers['AMP-Match'] = event.match
            response.headers['AMP-Session'] = event.session

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
            response_buffer.append("<b>Flushed buffer with ID %s.</b>" % None)
        response_buffer.append(u"<b>Prebuffer with ID %s of size:</b> %s" % (id(self.prebuffer), self.prebuffer.qsize()))

        # We're done processing. Flush buffer and respond.
        self.log("Tracker transaction completed. Writing body.")
        self.verbose("Tracker response buffer of length %s:" % len(response_buffer))
        self.verbose(str(response_buffer))
        response.text = u"\n".join(response_buffer)

        response.stage = protocol.ResponseStage.COMPLETE
        self.verbose('Yielding to server-side transport.')
        for chunk in response.app_iter:
            yield chunk
        raise StopIteration()
