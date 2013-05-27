# -*- coding: utf-8 -*-

'''
PubSub API: Service

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Local Imports
from . import messages
from . import exceptions

# apptools services / protorpc
from apptools import services
from protorpc import message_types

# apptools util
from apptools.util import datastructures

# API Service
from api.services import APIService


## PubSubService - exposes methods for publishing and subscribing to `TrackedEvent`(s).
class PubSubService(APIService):

    ''' Exposes methods for publishing and subscribing to the `TrackedEvent` stream. '''

    _config_path = 'hermes.api.tracker.PubSubAPI'

    exceptions = datastructures.DictProxy(**{
        'generic': exceptions.Error
    })

    @services.rpcmethod(messages.BatchPublish, message_types.VoidMessage)
    def publish(self, request):

        ''' Publish a message to the global eventstream. '''

        pass

    @services.rpcmethod(messages.BatchSubscribe, messages.BatchSubscribe)
    def subscribe(self, request):

        ''' Establish a new subscription to a channel. '''

        pass

    @services.rpcmethod(messages.Subscription, message_types.VoidMessage)
    def unsubscribe(self, request):

        ''' Close and destroy an existing subscription. '''

        pass
