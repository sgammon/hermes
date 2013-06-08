# -*- coding: utf-8 -*-

'''
Contains models used in the `EventTracker` subsystem that are specifically related to
fulfilling publish/subscribe infrastructure behind the global eventstream.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# apptools models
from apptools import model
from api.models import TrackerModel


## Subscription
# Represents a subscription to all/some `TrackedEvent` items.
class Subscription(TrackerModel):

    ''' A hit to the `EventTracker` server. '''

    channel = basestring, {'required': True, 'indexed': True}  # channel / named channel pattern expressed in Redis
    pattern = bool, {'default': False, 'indexed': True}  # whether we want to do a Psubscribe on the given channel
    expiration = int, {'default': -86400}  # value < 0 indicates relative expiration in seconds, > 0 is absolute
