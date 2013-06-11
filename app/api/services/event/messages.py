# -*- coding: utf-8 -*-

'''
Event Data API: Messages

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# apptools
from apptools import rpc
from apptools import model


## EventKeys
# Holds multiple keys for :py:class:`event.TrackedEvent` models.
class EventKeys(rpc.messages.Message):

    ''' Holds multiple keys for :py:class:`event.TrackedEvent`
        models. '''

    count = rpc.messages.IntegerField(1)
    keys = rpc.messages.MessageField(model.Key.to_message_model(), 2, repeated=True)


## EventRange
# Expresses a request for a range of :py:class:`event.TrackedEvent` models.
class EventRange(rpc.messages.Message):

    ''' Expresses a range of requested :py:class:`event.TrackedEvent`
        models, either as a request or a response. '''

    pass


## Events
# Container for a set of related :py:class:`event.TrackedEvent` entities.
class Events(rpc.messages.Message):

    ''' Container for expressing multiple :py:class:`event.TrackedEvent`
        entities. '''

    pass
