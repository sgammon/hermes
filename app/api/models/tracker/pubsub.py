# -*- coding: utf-8 -*-

'''

Tracker Models: PubSub

Contains models used in the `EventTracker` subsystem that are specifically related to
fulfilling publish/subscribe infrastructure behind the global eventstream.

-sam (<sam.gammon@ampush.com>)

'''

# apptools models
from apptools import model


## Subscription
# Represents a subscription to all/some `TrackedEvent` items.
class Subscription(model.Model):

    ''' A hit to the `EventTracker` server. '''

    channel = basestring, {'required': True}  # named channel / named channel pattern expressed in Redis
    pattern = bool, {'default': False}  # whether we want to do a Psubscribe on the given channel
    expiration = int, {'default': -86400}  # negative value indicates expiration relative to creation time by X seconds - positive values are interpreted absolutely
