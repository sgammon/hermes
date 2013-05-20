# -*- coding: utf-8 -*-

'''

Components: Tracker

This file contains the main `EventTracker` server, with accompanying
low-level WSGI logic to dispatch and double-buffer tracked events
to the `DatastoreEngine` component, for pipelined persistence to
Redis.

-sam (<sam.gammon@ampush.com>)

'''

# stdlib
import time

# 3rd party
import webob
import webapp2

# gevent
import gevent
from gevent import pool

# hermes codebase
import event
import protocol
import datastore

# hermes config
import config
from config import debug
from config import verbose
from config import _HEADER_PREFIX
from config import _PREBUFFER_FREQUENCY
from config import _PREBUFFER_THRESHOLD

# hermes util
from util import exceptions


# Globals
_TRACKER_VERSION = (0, 5)  # advertised in `AMP-Tracker` response header
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
            self.log("Debug mode is ON, serving on port %s." % config._DEVSERVER_PORT)

        # Allow overwriting the TrackedEvent implementation class
        if event:
            self.event_class = event  # pragma: no cover

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
            def _log_blackhole(message, force=False):

                ''' Drop invokee data if debug isn't enabled. '''

                if force:
                    return self._output(message)
                return
            return _log_blackhole
        else:
            def _log_debug(message, force=False):

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

    def begin_request(self, environ, start_response):

        ''' Factory a new `webob.Request`/`webob.Response` pair, representing a new HTTP transaction cycle. '''

        # grab content type
        content_type, encoding = self.content_type

        # provision request + response
        request = self.request_class(environ)
        response = self.response_class(content_type=content_type, charset=encoding)

        # fill-in response info
        response.stage = protocol.ResponseStage.PENDING
        response.request = request
        for hkey, hvalue in self._base_headers:
            response.headers[hkey] = hvalue

        if self.chunked:

            # remove Content-Length for a chunked response
            self.verbose('Running in CHUNKED mode, removing Content-Length header.')
            del response.headers['Content-Length']

        if verbose:
            self.verbose("Updated response headers: \"%s\"." % response.headers)
        return request, response

    def send_response(self, response, start_response, flush=False):

        ''' Send the WSGI start_response, optionally flushing the response buffer and finishing the transaction. '''

        if response.stage == protocol.ResponseStage.PENDING:

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

        # Spawn request + response
        request, response = self.begin_request(environ, start_response)

        try:
            # Factory new `TrackedEvent`.
            event = self.event_class.new(self, request, response)
            self.engine.inbox.put_nowait(event)  # send to datastore adapter immediately

            # Begin building headers.
            response.headers['%s-Match' % self.header_prefix] = event.match
            response.headers['%s-Session' % self.header_prefix] = event.session

            if verbose:
                self.verbose("Encountered match value %s with session %s." % (event.match, event.session))

        except exceptions.ClientError as e:

            # Handle 400-bound ClientError(s)
            response.status = 400
            self.error("Encountered ClientError: \"%s\". Raising HTTP400." % e)

            yield self.send_response(response, start_response, flush=True)
            raise StopIteration()

        except exceptions.PlatformError as e:

            # Handle 500-bound PlatformError(s)
            response.status = 500
            self.error("Encountered PlatformError: \"%s\". Raising HTTP500." % e)

            yield self.send_response(response, start_response, flush=True)
            raise StopIteration()

        except exceptions.Error as e:

            # Handle 500-bound critical errors.
            self.error("Encountered known (but unhandled) exception: \"%s\"." % e)
            self.error("Exception description: \"%s\"." % e.__doc__)

            response.status = 500
            yield self.send_response(response, start_response, flush=True)
            raise StopIteration()

        if verbose:
            self.verbose("Provisioned new `TrackedEvent` \"%s\". Starting deferred response." % event)

        # if `guess_response` returns `True`, we can return with no content and a blank 200.
        # otherwise, we defer to the event for full header processing.
        fast_response = event.guess_response(response)
        if fast_response:

            fast_response.stage = protocol.ResponseStage.COMPLETE

            # start response with appropriate headers
            response = self.send_response(fast_response, start_response, flush=True)

        else:
            response.stage = protocol.ResponseStage.COMPLETE

            # calculate event response
            response = self.send_response(event.respond(response), start_response, flush=True)
            yield response

        # We're done processing. Flush buffer and respond.
        self.log("Tracked event with ID \"%s\"." % event.id, force=True)

        gevent.sleep(0)
        raise StopIteration()
