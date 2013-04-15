# -*- coding: utf-8 -*-

'''

Models: Tracker

Contains models used in the `EventTracker` subsystem.

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
