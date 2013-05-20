# -*- coding: utf-8 -*-

'''
PubSub API: Messages

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# ProtoRPC
from protorpc import messages

# Hermes Models
from api.models.tracker.event import TrackedEvent
from api.models.tracker.pubsub import Subscription


## Publish - message that represents a request to publish a `TrackedEvent`.
class Publish(messages.Message):

    ''' Expresses a request to manually publish a `TrackedEvent` to the global eventstream. '''

    url = messages.StringField(1)
    event = messages.MessageField(TrackedEvent.to_message_model(), 2)
