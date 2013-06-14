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
import uuid
import hashlib
import datetime

# 3rd party
import webob

# apptools models
from apptools import model
from api.models import TrackerModel


## Event
# Represents a raw hit to a tracker URL.
class Event(TrackerModel):

    ''' Raw record of a :py:class:`TrackedEvent`. Only used in
        the case that the given event is recording hits to URLs -
        other forms of tracking use ``TrackedEvent`` directly. '''

    # == Basic Details == #
    url = basestring, {'required': True, 'indexed': False}  # full text of URL hit (including params + hash, if any)
    method = basestring, {'required': True, 'indexed': False}  # request method used to hit the URL that was invoked
    policy = basestring, {'indexed': True}  # hit came in and was processed by the specified policy

    # == Session Details == #
    session = bool, {'indexed': False}  # hit came in with a session (True) or one was created (False)
    fingerprint = basestring, {'indexed': True, 'indexed': False}  # plaintext value of the cookie in this event

    # == Flags == #
    error = bool, {'indexed': True, 'default': False}  # flag indicating this might be an error
    legacy = bool, {'indexed': True, 'default': False}  # flag indicating this is a legacy tracker hit
    processed = bool, {'indexed': False, 'default': False}  # whether this `RawEvent` has been processed yet

    # == Timestamps == #
    timestamp = datetime.datetime, {'required': True, 'indexed': True}  # timestamp for when this was received
    modified = datetime.datetime, {'required': True, 'auto_now': True}  # timestamp for when this was last modified
    created = datetime.datetime, {'required': True, 'auto_now_add': True}  # timestamp for when the raw event was saved

    @classmethod
    def inflate(cls, data, policy=None, legacy=False, timestamp=None):

        ''' Build a new :py:class:`Event` from a :py:class:`webapp2.Request`,
            or raw ``dict``.

            :param data: Source of data for inflating this :py:class:`Event`.
            Can be a :py:class:`webob.Request` or ``dict``. Required.

            :param policy: :py:class:`Profile` descendent class that was
            selected to process against this :py:class:`Event`. Defaults
            to ``None``.

            :param legacy: Flag (``bool``) indicating whether the current
            :py:class:`Event` was sent to a legacy or modern (*canonical form*)
            endpoint. Defaults to ``False``.

            :param timestamp: Timestamp to use as the earliest-known-time
            of record for the constructed :py:class:`Event`.

            :raises TypeError: In the case of an invalid type for ``data``.

            :raises ValueError: In the case that a required parameter for
            the inflation routine was found to be invalid.

            :returns: Constructed :py:class:`Event`. '''

        from policy import base

        # build timestamp if we're not handed one.
        timestamp = timestamp or datetime.datetime.now()

        if isinstance(data, webob.Request):

            # resolve unique event ID
            eid = data.headers.get('XAF-Hash')
            if not eid:
                eid = data.headers.get('XAF-Request-ID')
                if not eid:
                    eid = hashlib.sha256(str(uuid.uuid4())).hexdigest()  # bad news: hopefully we're in ``debug``

            url = data.url  # full HTTP request URL
            method = data.method  # HTTP request method

            # resolve _AMP cookie, or explicit session
            if base._DEFAULT_COOKIE_NAME in data.cookies:
                cookie = data.cookies.get('_amp')

        elif isinstance(data, dict):

            # resolve unique event ID (generate a random one via ``uuid4`` if we can't find a good one)
            eid = data.get('id', hashlib.sha256(str(uuid.uuid4())).hexdigest())
            url = data.get('url', None)  # try to grab URL
            method = data.get('method', None)  # try to grab method
            cookie = data.get('fingerprint', data.get('cookie', None))  # try to grab cookie

        else:

            # fail: we only accept ``webob.Request`` and ``dict``
            raise TypeError('Param `data` of `Event.inflate` must be a `dict` or `webob.Request`.')

        if not url:

            # fail: we require at least a URL if we're using the raw interface
            raise ValueError('Data property `url` of `Event` must not be null.')

        # build raw event
        return cls(**{
            'key': model.Key(cls, eid),  # key with assigned raw event ID
            'policy': policy.__definition__,  # grab definition path for matched policy
            'legacy': legacy,  # flag indicates whether this is a legacy hit
            'url': url,  # original URL invoking ``inflate``
            'method': method,  # original HTTP method, if any
            'cookie': cookie,  # original HTTP _amp cookie value, if any
            'modified': timestamp,  # timestamp of when this was last modified
            'timestamp': timestamp,  # timestamp of when this raw event was received
            'created': timestamp  # timestamp of when this raw event was first persisted
        })

    def notify_error(self, exception, message=None, handled=False, processed=False, put=False, pipeline=None):

        ''' Notify an existing :py:class:`Event` that an error
            occurred, which should generate a matching
            :py:class:`Error` entity and mark the current raw
            event as existing in a state of exception.

            :param exception: Python ``Exception`` descendent
            object describing the error state encountered while
            processing this :py:class:`Event`.

            :param message: Message ``str`` that, when given,
            will override any message acquired from ``exception``.

            :param handled: Flag (``bool``) indicating whether
            this exception was an expected case in the context
            which it was encountered in.

            :param processed: Flag (``bool``) indicating whether
            we finished processing the raw :py:class:`Event`
            before the error ocurred (indicating it ocurred in
            future stages and was updated retroactively).

            :param put: Flag (``bool``) indicating whether invoking
            callees desire the generated :py:class:`Error` child
            entity to be persisted immediately upon construction.

            :param pipeline: Low-level datastore pipeline to use
            for persisting the constructed :py:class:`Error`, if
            persistence is requested (via ``put``). Has no effect
            if ``put`` evaluates to *falsy*, or the underlying
            datastore adapter lacks support for pipelining.

            :returns: Tupled pair of this raw event and the
            generated :py:class:`Error`, like ``(self, error)``. '''

        # set local error state
        self.error, self.processed, error = True, processed, Error(**{
            'key': model.Key(Error, parent=self.key),
            'code': exception.__class__.__name__,
            'message': message or str(exception),
            'handled': handled
        })

        if put: error.put(pipeline=pipeline)

        # build sub-error and return
        return self, error


## Error
# Represents an error event that occurred.
class Error(TrackerModel):

    ''' Primitive record of an error event. Spawned via the model
        method :py:meth:`Event.notify_error`, which fills in a
        child key and exception details. '''

    code = basestring  # error code, if any (or exception name)
    event = basestring, {'indexed': True}  # raw event that generated this error
    message = basestring  # message associated with error
    handled = bool, {'default': False}  # whether this was unexpected
