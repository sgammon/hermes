# -*- coding: utf-8 -*-

'''
Raw Data API: Messages

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# ProtoRPC
from apptools import rpc
from apptools import model

# Raw Models
from api.models.tracker import raw


## RawKeys
# Holds multiple raw event keys.
class RawKeys(rpc.messages.Message):

    ''' Holds a set of raw event keys to be
        retrieved or altered in batch. '''

    keys = rpc.messages.MessageField(1, model.Key.to_message_model(), repeated=True)


## RawEvents
# Holds multiple :py:class:`raw.Event` models.
class RawEvents(rpc.messages.Message):

    ''' Holds a set of :py:class:`raw.Event` models
        that result from a call to retrieve multiple
        raw events by key or range value. '''

    count = rpc.messages.IntegerField(1)
    events = rpc.messages.MessageField(2, raw.Event.to_message_model(), repeated=True)
