# -*- coding: utf-8 -*-

'''
Raw Data API: Service

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Local Imports
from . import messages
from . import exceptions

# apptools services
from apptools import rpc
from apptools import model

# Raw Models
from api.models.tracker import raw


## RawDataService - exposes methods for retrieving raw data from `EventTracker`.
@rpc.service
class RawDataService(rpc.Service):

    ''' Exposes methods for retrieving raw data from `EventTracker`. '''

    name = 'raw'
    _config_path = 'hermes.api.tracker.RawDataAPI'

    exceptions = rpc.Exceptions(**{
        'generic': exceptions.Error
    })

    @rpc.method(model.Key, raw.Event)
    def get(self, request):

        ''' Retrieve a :py:class:`raw.Event` by its associated
            :py:class:`model.Key`. '''

        pass

    @rpc.method(messages.RawKeys, messages.RawEvents)
    def get_multi(self, request):

        ''' Retrieve multiple :py:class:`raw.Event` entities
            in batch. '''

        pass

    @rpc.method(rpc.messages.VoidMessage, messages.RawEvents)
    def get_all(self, request):

        ''' Retrieve all known :py:class:`raw.Event` entities. '''

        pass
