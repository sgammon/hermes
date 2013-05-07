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


## TrackedEvent
# Represents a single `EventTracker` URL hit.
class TrackedEvent(model.Model):

    ''' A hit to the `EventTracker` server. '''

    id = basestring, {'required': True, 'indexed': True}
    type = basestring, {'required': True, 'indexed': True}
    params = dict, {'required': True}
    raw_url = basestring, {'required': True}
    timestamp = datetime.datetime, {'required': True, 'indexed': True}
    modified = int, {'default': lambda x: time.time(), 'indexed': True}
