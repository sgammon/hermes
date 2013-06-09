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
from api.models import TrackerModel


## Event
# Represents a raw hit to a tracker URL.
class Event(TrackerModel):

    ''' Raw record of a `TrackedEvent`. '''

    url = basestring, {'required': True, 'indexed': False}  # full text of URL hit (including params + hash, if any)
    method = basestring, {'required': True, 'indexed': True}  # request method used to hit the URL that was invoked
    session = bool, {'indexed': True}  # hit came in with a session (True) or one was created (False)
    policy = basestring, {'indexed': True}  # hit came in and was processed by the specified policy
    processed = bool, {'indexed': True}  # whether this `RawEvent` has been processed yet
    cookie = basestring, {'indexed': True, 'indexed': True}  # plaintext value of the cookie in this event
    legacy = bool, {'indexed': True}  # flag indicating this is a legacy tracker hit
    error = bool, {'indexed': True}  # flag indicating this might be an error
    modified = datetime.datetime, {'required': True, 'auto_now': True}  # timestamp for when this was last modified
    timestamp = datetime.datetime, {'required': True, 'auto_now_add': True}  # timestamp for when this was created

    @classmethod
    def inflate(cls, request, policy=None, legacy=False):

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
            'policy': policy.__definition__,
            'legacy': legacy,
            'modified': now,
            'timestamp': now
        })

        # resolve _AMP cookie, or explicit session
        if '_amp' in request.cookies:
            event.cookie = request.cookies.get('_amp')

        return event


## Error
# Represents an error event that occurred.
class Error(TrackerModel):

    ''' Primitive record of an error event. '''

    code = basestring  # error code, if any
    event = Event, {'indexed': True}  # raw event that generated this error
    message = basestring  # message associated with error
    exception = basestring  # exception name associated with error
    unhandled = bool, {'default': False}  # whether this was unexpected
