# -*- coding: utf-8 -*-

'''
The :py:class:`EventBuilder` class handles the construction and
interpretation of :py:class:`model.event.TrackedEvent` entities.
Execution flow for collapsing :py:class`model.profile.EventProfile`
records and gathering followup tasks happens here - although it
is enforced by :py:class:`platform.ampush.tracker.policy.PolicyEngine`.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Tracker Models
from api.models.tracker.raw import Event

# Platform Parent
from api.platform import PlatformBridge


## EventBuilder - handles the construction of ``TrackedEvent`` records.
class EventBuilder(PlatformBridge):

    ''' Manages the inflation, construction, and
        interpretation of ``TrackedEvent`` entities. '''

    def raw(self, request, propagate=True, policy=None, legacy=False):

        ''' Entrypoint for recording raw events and producing
            :py:class:`model.raw.Event`.

            If requested, this method will also produce a ``guess``
            as to how the request can be handled, if any. Available
            ``guess`` options are enumerated in a bidirectional
            protocol enum at :py:class:`protocol.flow.ResponseVector`.

            :param request: The current :py:class:`webapp2.Request`, or a
            valid :py:class:`model.raw.Event` to inject directly into the
            raw eventstream.

            :keyword propagate: Flag indicating that this event should be
            propagated to the global eventstream. Defaults to ``True``.

            :keyword policy: The currently-matched policy suite that is
            expected to fulfill service for this hit.

            :keyword legacy: Flag indicating this hit is a legacy event,
            and will not have an attached tracker.

            :returns: Published (and possibly new) :py:class:`model.raw.Event`,
                      and, if requested via ``live``, a guess about how to
                      handle the request, like: ``tuple(<event>, <guess>)``. '''

        # inflate raw event & publish to pubsub
        raw = Event.inflate(request, policy, legacy)
        raw.put()

        return self.bus.stream.publish(raw, propagate=propagate)

    def error(self, event, reason="Unknown reason.", propagate=True):

        ''' Register a :py:class:`model.raw.Event` or a full
            :py:class:`model.event.TrackedEvent` as a potential
            error event.

            :param event: The event to register in the error
                          eventstream.

            :keyword reason: String reason describing why this
                             event was found to be an error.

            :keyword propagate: Flag indicating whether this
                                error event is happening live
                                and should be propagated to
                                the global eventstream.
                                Defaults to ``True``.

            :returns: The ``event`` it was handed, for chainability. '''

        self.bus.stream.publish(event, error=True)
        pass
