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

# Platform Parent
from api.platform import PlatformBridge


## EventStream - handles propagation and dispatch of eventstream data.
class EventStream(PlatformBridge):

    ''' Manages state for global (and contextual) event
        streams in ``EventTracker``. '''

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

    def publish(self, event, error=False, propagate=True):

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

            :returns: Result of the low-level ``publish`` routine. '''

        # convert event to a message
        event = event.to_message()

        # wrap in an event message and publish
        self.bus.engine.publish()

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
