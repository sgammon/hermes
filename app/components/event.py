# -*- coding: utf-8 -*-

'''
Components: Events

This file contains `TrackedEvent`, a class used to represent
individual events tracked by the `EventTracker`.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# stdlib
import time

# hermes codebase
import protocol
from config import debug
from config import _PARAM_SEPARATOR
from config import _DISCARD_NOSENTINEL

# hermes util
from util import exceptions


## Param sets
InternalParams = frozenset([protocol.BuiltinParameters.DEBUG, protocol.BuiltinParameters.DRYRUN, protocol.BuiltinParameters.SENTINEL])
AmpushParams = frozenset([protocol.BuiltinParameters.REF, protocol.BuiltinParameters.TYPE])
AllParams = frozenset([getattr(protocol.BuiltinParameters, i) for i in protocol.BuiltinParameters.__dict__ if not i.startswith('_')])


## TrackedEvent - a conversion, impression, etc
class TrackedEvent(object):

    ''' Represents a hit to a tracked event. '''

    id = None  # unique ID for this event
    path = None  # URL path being requested
    match = None  # quickmatch result, if any
    error = None  # records a deferred error
    params = {}  # filtered URL query parameters
    cookie = None  # `amp` cookie value
    request = None  # current webob request
    session = None  # current/established session
    tracker = None  # reference to parent tracker
    response = None  # current webob response
    sentinel = False  # sentinel compliance flag

    @classmethod
    def new(cls, tracker, request, response):

        ''' Factory for a `TrackedEvent`. '''

        # Copy in request, path and params
        path, params = request.path, dict(request.params)
        return cls(tracker, request, params, response)

    def __init__(self, tracker, request, params, response):

        ''' Initialize this `TrackedEvent`. '''

        # Initialize WSGI request/response properties
        self.tracker, self.request, self.path, self.params, self.response = tracker, request, request.path, params, response

        # Perform pre-validation
        if self.param(protocol.BuiltinParameters.SENTINEL) not in self.params:
            self.sentinel = False
            if not _DISCARD_NOSENTINEL:
                # Just warn if we're in debug...
                self.tracker.warn("Not using the Sentinel value can cause bad counts. (Sentinel param is currently '%s'.)" % self.param(protocol.TrackerProtocol.SENTINEL))
            else:
                self.tracker.error("No sentinel found, running in strict sentinel mode. (Sentinel param is currently '%s'.)" % self.param(protocol.TrackerProtocol.SENTINEL))
                raise exceptions.InvalidSentinel("Sentinel key not found in tracker URL - event refused.")
        else:
            # Indicate we *do* have a sentinel
            self.tracker.verbose("Sentinel value found.")
            self.sentinel = True

        # Generate computed properties
        self.decode().generate_id(id(self))

    @property
    def debug(self):

        ''' Indicate whether we're in debug mode (globally or per-request). '''

        return (debug or (self.param(protocol.BuiltinParameters.DEBUG) in self.request.params))

    def param(self, name):

        ''' Get or set the value of a URL param. '''

        # If it's an Ampush param, add the prefix...
        if name in AmpushParams:
            param = _PARAM_SEPARATOR.join((protocol.TrackerPrefix.AMPUSH, name))

        # Same if it's an Internal param...
        elif name in InternalParams:
            param = _PARAM_SEPARATOR.join((protocol.TrackerPrefix.INTERNAL, name))

        # Otherwise, it's custom.
        else:
            param = _PARAM_SEPARATOR.join((protocol.TrackerPrefix.CUSTOM, name))

        return param

    def generate_id(self, base):

        ''' Generate a proper unique ID for this event. '''

        id = self.request.headers.get('XAF-Hash')
        if not id:
            id = self.request.headers.get('XAF-Request-ID')
            if not id:
                id = '-'.join([str(base), str(int(time.time()))])
        self.id = id
        return self

    def decode(self, injected=None):

        ''' Decode an existing session, if any, or use `injected`. '''

        return self

    def build(self, salt=None, pepper=None):

        ''' Build a new local session, and return the new session ID. '''

        pass

    @property
    def session(self):

        ''' Retrieve the current session object, or if there isn't one, build it anew. '''

        return "_SESSION_"

    @property
    def match(self):

        ''' Retrieve any identified session matches. '''

        return self.seen()

    def serialize(self):

        ''' Serialize this TrackedEvent into numerous Redis writes. '''

        data = {
            '-'.join(['event', self.id]): [('id', self.id), ('type', 'test'), ('timestamp', str(time.time()))] + self.params.items()
        }

        return (data, self.generate_indexes())

    def generate_indexes(self):

        ''' Generate index writes for a given `TrackedEvent`. '''

        return tuple()

    def seen(self):

        ''' Read Redis to see if we know this to be a match. '''

        return 'NONE'

    def respond(self, response):

        ''' Respond to the client that generated this event. '''

        return response

    def guess_response(self, request):

        ''' Quickly try and guess a response type that can immediately be sent. '''

        return None
