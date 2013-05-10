# -*- coding: utf-8 -*-

'''

PubSub API: Service

-sam (<sam.gammon@ampush.com>)

'''

# Base Imports
import config
import webapp2

# Local Imports
from . import messages
from . import exceptions

# apptools services / protorpc
from apptools import services
from protorpc import message_types

# apptools util
from apptools.util import debug
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

    @webapp2.cached_property
    def config(self):

        ''' Cached access to `PubSubService` config. '''

        return config.config.get(self._config_path, {'debug': False})

    @webapp2.cached_property
    def logging(self):

        ''' Cached access to dedicated log pipe. '''

        path = self._config_path.split('.')
        return debug.AppToolsLogger(path='.'.join(path[0:-1]), name=path[-1])._setcondition(self.config.get('debug'))

    @services.rpcmethod(messages.Publish, messages.TrackedEvent)
    def publish(self, request):

        ''' Publish a `TrackedEvent` to the global eventstream. '''

        pass

    @services.rpcmethod(messages.Subscription, messages.Subscription)
    def subscribe(self, request):

        ''' Subscribe  '''

        pass

    @services.rpcmethod(messages.Subscription, message_types.VoidMessage)
    def unsubscribe(self, request):

        '''  '''

        pass