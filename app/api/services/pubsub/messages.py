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
from api.models.tracker.raw import Event
from api.models.tracker.event import TrackedEvent
from api.models.tracker.pubsub import Subscription


## LogMessage - generic message for expressing a string to be published as a log.
class LogMessage(messages.Message):

    ''' Expresses a generic log message to be published. '''

    content = messages.StringField(1, required=True)
    prefix = messages.StringField(2, default='Log')


## Publish - message that represents a request to publish a `TrackedEvent`.
class Publish(messages.Message):

    ''' Expresses a request to manually publish a `TrackedEvent` to the global eventstream. '''

    class PayloadType(messages.Enum):

        ''' Enumerates possible :py:class:`Publish` types. '''

        RAW = 0x1  # indicates a raw event (:py:class:`api.models.tracker.raw.Event`)
        INTERPRETED = 0x2  # indicates a full event (:py:class:`api.models.tracker.event.TrackedEvent`)
        LOG = 0x3  # indicates a generic log message to publish

    class ChannelSpec(messages.Message):

        ''' Specifies a set of channels to publish this message to. '''

        class ChannelFlags(messages.Enum):

            ''' Enumerates flags describing channel publish behavior. '''

            GLOBAL = 0x1  # in addition to channels specified, publish to the global stream
            ERROR = 0x2  # mark this published message as an error notification
            PROPAGATE = 0x3  # propagate this event/raw event to higher-order streams
            CUSTOM = 0x4  # this publish operation contains explicit, custom channels

        # name and channel flags
        name = messages.StringField(1, required=True)  # name of the channel being specified
        data = messages.BooleanField(2, default=True)  # whether to publish the key or full data blob
        flags = messages.EnumField(ChannelFlags, 3, repeated=True)

    ## basic details
    kind = messages.EnumField(PayloadType, 1, default=PayloadType.LOG)
    raw = messages.MessageField(Event.to_message_model(), 2)
    event = messages.MessageField(TrackedEvent.to_message_model(), 3)
    message = messages.MessageField(LogMessage, 4)
    channels = messages.MessageField(ChannelSpec, 5, repeated=True)
    timestamp = messages.StringField(6)


## BatchPublish - message that represents a batch of publish requests.
class BatchPublish(messages.Message):

    ''' Expresses a batch of :py:class:`Publish` requests. '''

    count = messages.IntegerField(1)
    payload = messages.MessageField(Publish, 2, repeated=True)


## BatchSubscribe - message that represents a batch of subscription requests.
class BatchSubscribe(messages.Message):

    ''' Expresses a batch of :py:class:`Subscription` requests. '''

    count = messages.IntegerField(1)
    subscriptions = messages.MessageField(Subscription.to_message_model(), 2, repeated=True)
