# -*- coding: utf-8 -*-

'''
Contains models used in the `EventTracker` subsystem that are specifically related to
expressing/persisting individual events.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# apptools models
from apptools import model

# protocol descriptors
from protocol import event

# tracker models
from api.models import TrackerModel


## TrackedEvent
class TrackedEvent(TrackerModel):

    ''' A single hit to the ``EventTracker`` server, linked to a :py:class:`tracker.Tracker`
        model via a string ID, and containing *n* parameters. Individual :py:class:`TrackedEvent`
        models detail an individual tracking hit, with all associated information and metadata
        about aggregations and attributions.

        :param raw: Reference :py:class:`apptools.model.Key` to the :py:class:`raw.RawEvent`
        that generated this particular :py:class:`TrackedEvent`.

        :param params: Python ``dict`` describing the **interpreted** parameters for this
        ``TrackedEvent``. For *raw* parameters, see :py:class:`raw.RawEvent`.

        :param type: Describes the type of event being recorded in this :py:class:`TrackedEvent`,
        such as a ``CLICK`` or ``IMPRESSION``. These are enumerated in the bidirectional
        enum :py:class:`event.EventType`.

        :param tracker: Reference :py:class:`apptools.model.Key` to the :py:class:`tracker.Tracker`
        that recorded this :py:class:`TrackedEvent`.

        :param provider: Describes the *provider* that relayed this event to Ampush, if any. Available
        providers are enumerated in the bidirectional enum :py:class:`event.EventProvider`.

        :param aggregations: Lists *aggregation groups* that this :py:class:`TrackedEvent` was found to
        be a part of. Aggregation groups listed in this area have already considered
        this :py:class:`TrackedEvent`.

        :param attributions: Lists *attribution groups* that this :py:class:`TrackedEvent` was linked to.
        Aggregation groups listed in this area have already linked and considered this :py:class:`TrackedEvent`.

        :param modified: Timestamp ``datetime`` of the last time this :py:class:`TrackedEvent` was modified.

        :param created: Timestamp ``datetime`` of when this :py:class:`TrackedEvent` was recorded. '''

    ## == Raw Event == ##
    raw = basestring, {'required': True, 'indexed': True}  # linked raw event that generated this `TrackedEvent`
    params = dict, {'required': True, 'default': {}, 'indexed': False}  # raw paramset that came through with URL

    ## == Type/Provider/Tracker == ##  # @TODO: Change string types to enums.
    type = event.EventType, {'indexed': True, 'default': 'CUSTOM'}  # event type: impression, click, etc.
    error = bool, {'indexed': True}  # error flag: flipped to ``True`` if an error was detected while processing
    tracker = basestring, {'indexed': True}  # provisioned tracker that this event came through

    ## == Messages == ##
    errors = basestring, {'repeated': True, 'indexed': False}  # error messages encountered processing this event
    warnings = basestring, {'repeated': True, 'indexed': False}  # warning messages encountered processing this event

    ## == Linked Objects == ##
    integrations = basestring, {'repeated': True, 'indexed': True}  # linked, invoked integrations
    aggregations = basestring, {'repeated': True, 'indexed': True}  # linked, updated aggregations
    attributions = basestring, {'repeated': True, 'indexed': True}  # linked, attributed events/objects
