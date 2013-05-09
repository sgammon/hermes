# -*- coding: utf-8 -*-

'''

Tracker Models: Event

Contains models used in the `EventTracker` subsystem that are specifically related to
expressing/persisting individual events.

-sam (<sam.gammon@ampush.com>)

'''

# stdlib
import time
import datetime

# apptools models
from apptools import model

# tracker models
from api.models.tracker import raw
from api.models.tracker import tracker
from api.models.tracker import integration
from api.models.tracker import aggregation
from api.models.tracker import attribution

# protocol modules
from components.protocol import event


## EventAction
# Represents an action taken in response to an event.
class EventAction(model.Model):

    ''' An action performed by the `EventTracker` in response to an occurrence of a `TrackedEvent`. '''

    success = bool, {'default': False, 'indexed': True}  # whether this `EventAction` was successful
    started = datetime.datetime, {'required': False, 'indexed': True}  # timestamp for when this `EventAction` started work
    routine = integration.Routine, {'repeated': True, 'indexed': True}  # linked routine set to fulfill this `EventAction`


## TrackedEvent
# Represents a single `EventTracker` URL hit.
class TrackedEvent(model.Model):

    ''' A hit to the `EventTracker` server. '''

    ## == Raw Event == ##
    raw = raw.RawEvent, {'required': True, 'indexed': True}  # linked raw event that generated this `TrackedEvent`
    params = dict, {'required': True, 'default': {}, 'indexed': False}  # raw paramset that came through with URL

    ## == Type/Provider/Tracker == ##
    type = event.EventType, {'indexed': True, 'default': event.EventType.CUSTOM}  # event type: impression, click, etc.
    tracker = tracker.Tracker, {'required': True, 'indexed': True}  # provisioned tracker that this event came through
    provider = event.EventProvider, {'indexed': True, 'default': event.EventProvider.CLIENT}  # event provider: who dispatched this event

    ## == Linked Objects == ##
    aggregations = aggregation.Aggregation, {'repeated': True, 'indexed': True}  # linked, updated aggregations
    attributions = attribution.Attribution, {'repeated': True, 'indexed': True}  # linked, attributed events/objects

    ## == Timestamps == ##
    modified = datetime.datetime, {'auto_now': True, 'indexed': True}  # timestamp for when this was last modified
    created = datetime.datetime, {'auto_now_add': True, 'indexed': True}  # timestamp for when this was created
