# -*- coding: utf-8 -*-

'''

Tracker Models: Event

Contains models used in the `EventTracker` subsystem that are specifically related to
expressing/persisting individual events.

-sam (<sam.gammon@ampush.com>)

'''

# apptools models
from apptools import model


## TrackedEvent - represents a single `EventTracker` URL hit.
class TrackedEvent(model.Model):

    ''' A hit to the `EventTracker` server. '''

    id = basestring, {'required': True}
    type = basestring
    profile = basestring, {'default': None}
    params = dict, {'required': True}
    timestamp = int, {'required': True}
