# -*- coding: utf-8 -*-

'''
Contains models used in the `EventTracker` subsystem that are specifically related to
expressing/persisting individual events.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# stdlib
import time
import datetime

# apptools models
from apptools import model

# tracker models
from api.models.tracker import raw
from api.models.tracker import endpoint
from api.models.tracker import integration
from api.models.tracker import aggregation
from api.models.tracker import attribution


## EventAction
# Represents an action taken in response to an event.
class EventAction(model.Model):

    ''' An action performed by the `EventTracker` in response to an occurrence of a `TrackedEvent`.

        :param success: Boolean describing whether the :py:class:`EventAction` in
                        question was successful or not. Defaults to ``False``.

        :param started: Python ``datetime`` object describing when this
                        :py:class:`EventAction` began execution.

        :param routine: Key pointer to the owner :py:class:`integration.Routine` object for this
                        :py:class:`EventAction`. '''

    success = bool, {'default': False, 'indexed': True}  # whether this `EventAction` was successful
    started = datetime.datetime, {'required': False, 'indexed': True}  # timestamp for when this `EventAction` started work
    routine = integration.Routine, {'repeated': True, 'indexed': True}  # linked routine set to fulfill this `EventAction`


## TrackedEvent
# Represents a single `EventTracker` URL hit.
class TrackedEvent(model.Model):

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
                             Aggregation groups listed in this area have already linked and considered
                             this :py:class:`TrackedEvent`.

        :param modified: Timestamp ``datetime`` of the last time this :py:class:`TrackedEvent` was modified.
        :param created: Timestamp ``datetime`` of when this :py:class:`TrackedEvent` was recorded. '''

    ## == Raw Event == ##
    raw = raw.Event, {'required': True, 'indexed': True}  # linked raw event that generated this `TrackedEvent`
    params = dict, {'required': True, 'default': {}, 'indexed': False}  # raw paramset that came through with URL

    ## == Type/Provider/Tracker == ##  # @TODO: Change string types to enums.
    type = str, {'indexed': True, 'default': 'CUSTOM'}  # event type: impression, click, etc.
    tracker = endpoint.Tracker, {'required': True, 'indexed': True}  # provisioned tracker that this event came through
    provider = str, {'indexed': True, 'default': 'CLIENT'}  # event provider: who dispatched this event

    ## == Linked Objects == ##
    integrations = EventAction, {'repeated': True, 'indexed': True}  # linked, invoked integrations
    aggregations = aggregation.Aggregation, {'repeated': True, 'indexed': True}  # linked, updated aggregations
    attributions = attribution.Attribution, {'repeated': True, 'indexed': True}  # linked, attributed events/objects

    ## == Timestamps == ##
    modified = datetime.datetime, {'auto_now': True, 'indexed': True}  # timestamp for when this was last modified
    created = datetime.datetime, {'auto_now_add': True, 'indexed': True}  # timestamp for when this was created
