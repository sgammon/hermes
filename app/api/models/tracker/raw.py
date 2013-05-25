# -*- coding: utf-8 -*-

'''
These models are used to express raw tracker events, before they are processed
into full `TrackedEvent` entities.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# stdlib
import hashlib
import datetime

# apptools models
from apptools import model


## Event
# Represents a raw hit to a tracker URL.
class Event(model.Model):

    ''' Raw record of a `TrackedEvent`. '''

    __adapter__ = "RedisAdapter"

    url = basestring, {'required': True, 'indexed': False}  # full text of URL hit (including params + hash, if any)
    method = basestring, {'required': True, 'indexed': True}  # request method used to hit the URL that was invoked
    session = bool, {'default': False, 'indexed': True}  # whether the request came in with a session (True) or one was created (False)
    processed = bool, {'default': False, 'indexed': True}  # whether this `RawEvent` has been processed into a `TrackedEvent` yet
    cookie = basestring, {'indexed': True, 'indexed': True}  # plaintext value of the cookie in this event
    error = bool, {'default': False, 'indexed': True}  # flag indicating this might be an error
    modified = datetime.datetime, {'required': True, 'auto_now': True}  # timestamp for when this record was last modified
    timestamp = datetime.datetime, {'required': True, 'auto_now_add': True}  # timestamp for when this record was created

    @classmethod
    def inflate(cls, request):

        ''' Build a new :py:class:`Event` from a :py:class:`webapp2.Request`,
            or a similar-style context object. '''

        # provision empty event
        now = datetime.datetime.now()

        # resolve unique event ID
        eid = request.headers.get('XAF-Hash')
        if not eid:
            eid = request.headers.get('XAF-Request-ID')
            if not eid:
                eid = hashlib.sha256(str(id(request))).hexdigest()  # bad news: hopefully we're in ``debug``

        event = cls(**{
            'key': model.Key(cls.kind(), eid),
            'method': request.method,
            'url': request.url,
            'modified': now,
            'timestamp': now
        })

        # resolve _AMP cookie, or explicit session
        if '_amp' in request.cookies:
            event.cookie = request.cookies.get('_amp')

        return event


## Error
# Represents an error event that occurred.
class Error(model.Model):

    ''' Primitive record of an error event. '''

    code = basestring  # error code, if any
    event = Event, {'indexed': True}  # raw event that generated this error
    message = basestring  # message associated with error
    exception = basestring  # exception name associated with error
    unhandled = bool, {'default': False}  # whether this was unexpected
