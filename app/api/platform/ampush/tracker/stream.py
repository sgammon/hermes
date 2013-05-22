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

    def publish(self, event, propagate=True):

        ''' Publish an event to one or more streams. Descendents of
            both :py:class:`models.tracker.event.RawEvent` and
            :py:class:`models.tracker.event.TrackedEvent` are supported
            for publishing.

            :param event: :py:class:`models.tracker.event.RawEvent` or
                          :py:class:`models.tracker.event.TrackedEvent` to
                          publish.
            :param propagate: Boolean (defaulting to ``True``) indicating
                              whether this publish should propagate globally. '''

        pass

    def subscribe(self, stream=None):
        pass
