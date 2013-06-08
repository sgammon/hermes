# -*- coding: utf-8 -*-

'''
The :py:class:`EventStream` class handles calls to publish
and subscribe to global or contextual streams of events
from ``EventTracker``.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# stdlib
import hashlib

# Models
from api.models.tracker import raw
from api.models.tracker import event

# Platform Parent
from api.platform import PlatformBridge


## EventStream - handles propagation and dispatch of eventstream data.
class EventStream(PlatformBridge):

    ''' Manages state for global (and contextual) event
        streams in ``EventTracker``. '''

    def _build_envelope(self, message, error=False):

        ''' Build and serialize an envelope and wrapped event,
            such that it is suitable for publishing via pub/sub.

            :param message: ``protorpc.Message``, due to be
                            published via pub/sub.

            :keyword error: Flag indicating this message is
                            an error. Defaults to ``False``.

            :returns: A ``dict`` representing the wrapped,
                      serialized ``protorpc.Message``. '''

        if hasattr(message, 'id') and message.id is not None:
            eid = message.id
        else:
            if hasattr(message, 'key') and message.key is not None:
                eid = message.key.id
            else:
                eid = str(id(message))

        return {
            'id': hashlib.sha512(eid).hexdigest(),
            'type': 'error' if error else message.__class__.__name__,
            'payload': message
        }

    def _generate_channels(self, blob, context=tuple(), error=False, propagate=True):

        ''' Generate a set of channels to publish to, given
            a blobbed blob to publish.

            :param blob: ``dict``, due to be published
                         via pub/sub.

            :param context: Iterable containing key=>value pairs
                            for other channel permutations to
                            publish on.

            :keyword error: Flag ``bool`` that indicates whether
                            we are generating error channels.
                            Defaults to ``False``.

            :keyword propagate: Flag ``bool`` that indicates
                                whether we should propagate
                                this event to higher-order
                                eventstreams. Defaults to
                                ``True``.

            :returns: A list of channels to publish the given
                      ``blob`` to. '''

        channels = []
        channel_template = ['__channel__']
        blobtype = blob.get('type', 'msg')

        if error:
            stream_type = 'error'  # publish to error stream for errors
        else:
            stream_type = 'stream'  # publish to regular stream for non-errors

        # first, zoom in
        if context:
            bundles = []
            for bundle in context:
                if isinstance(bundle, tuple):  # it's a key=>value pair
                    bundle = '-'.join(bundle)
                bundles.append('::'.join([bundle, stream_type]))

            for bundle in bundles:
                channels.append('::'.join(channel_template + [blobtype, bundle]))

        # now zoom out
        if propagate:

            # type-scoped channel
            channels.append('::'.join(channel_template + [blobtype, stream_type]))

            # global stream-scoped channel
            channels.append('::'.join(channel_template + ['__global__', stream_type]))

        return channels

    def stats(self):

        ''' Retrieve statistics about the desired *Event Stream*.
            Will return basic stuff like current rate-per-minute,
            message counter, last message timestamp and client list.

            :param channel: String channel name to retrieve stats for.
                            Passing ``None`` indicates a desire for
                            global *Event Stream* statistics.

            :raises ValueError: In the case of an invalid or unknown
                                channel.

            :returns: Record ``dict`` describing the requested statistics,
                      like: ``{'rate': 50, 'count': 100, 'clients': {'count': 2, 'list': ['one', 'two']}}`` '''

        pass

    def publish(self, ev, error=False, propagate=True):

        ''' Publish an event to one or more streams. Descendents of
            both :py:class:`models.tracker.event.RawEvent` and
            :py:class:`models.tracker.event.TrackedEvent` are supported
            for publishing.

            :param event: :py:class:`models.tracker.event.RawEvent` or
                          :py:class:`models.tracker.event.TrackedEvent` to
                          publish.

            :param error: Indicates that we're publishing an event describing
                          the attached hit as an ``error``. Defaults to ``False``
                          in a humerous attempt at optimism.

            :param propagate: Boolean (defaulting to ``True``) indicating
                              whether this publish should propagate globally.

            :returns: The ``event`` that was handed in and published. '''

        # convert event to a message
        blobbed_event = self._build_envelope(ev.to_message(), error)

        # build context
        if isinstance(ev, raw.Event):
            context = ['raw']

        elif isinstance(ev, event.TrackedEvent):
            context = [('stream', 'full')]

        else:
            context = tuple()

        # distribute to appropriate channels
        self.bus.engine.publish(self._generate_channels(blobbed_event, context, error, propagate), blobbed_event)

        return ev

    def subscribe(self, stream=None, _start=True):

        ''' Subscribe to one-or-more event streams in ``EventTracker``.
            Channels are persistently subscribed-to via ``Redis`` pubsub.

            Iterables, strings, regexes (for ``PSUBSCRIBE``) and ``None``
            are acceptable as streams - ``None`` indicates a subscription
            to the global *Event Stream*.

            :param stream: String channel name (``"coolchannel"``), regex channel name
                           (``r"coolch*"``) or iterable of those. Defaults to ``None``,
                           indicating a global ``EventTracker`` subscription is desired.

            :keyword _start: Immediately schedule the subscription ``Greenlet`` for
                             execution, before returning. Defaults to ``True``.

            :returns: Result of the low-level subscribe operation, and the new ``Greenlet``
                      which will do the listening. '''

        pass
