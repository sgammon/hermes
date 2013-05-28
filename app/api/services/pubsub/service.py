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

# apptools rpc
from apptools import rpc


## PubSubService - exposes methods for publishing and subscribing to `TrackedEvent`(s).
@rpc.service
class PubSubService(rpc.Service):

    ''' Exposes methods for publishing and subscribing to the `TrackedEvent` stream. '''

    _config_path = 'hermes.api.tracker.PubSubAPI'

    exceptions = rpc.Exceptions(**{
        'generic': exceptions.Error
    })

    @rpc.method(messages.BatchPublish, rpc.messages.VoidMessage)
    def publish(self, request):

        ''' Publish a message to the global eventstream. '''

        pass

    @rpc.method(messages.BatchSubscribe, messages.BatchSubscribe)
    def subscribe(self, request):

        ''' Establish a new subscription to a channel. '''

        pass

    @rpc.method(messages.Subscription, rpc.messages.VoidMessage)
    def unsubscribe(self, request):

        ''' Close and destroy an existing subscription. '''

        pass

