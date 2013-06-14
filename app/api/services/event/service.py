# -*- coding: utf-8 -*-

'''
Event Data API: Service

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
from apptools import model

# API Models
from api.models.tracker import event


## EventDataService - exposes methods for extracting data from `EventTracker`.
@rpc.service
class EventDataService(rpc.Service):

    ''' Exposes methods for interacting with & extracting data from `EventTracker`. '''

    name = 'event'
    _config_path = 'hermes.api.tracker.EventDataAPI'

    exceptions = rpc.Exceptions(**{
        'generic': exceptions.Error
    })

    @rpc.method(model.Key, event.TrackedEvent)
    def get(self, request):

        ''' Retrieve a :py:class:`event.TrackedEvent` model
            by its associated :py:class:`model.Key`. '''

        pass

    @rpc.method(messages.EventKeys, messages.Events)
    def get_multi(self, request):

        ''' Retrieve multiple :py:class:`event.TrackedEvent`
            models by their associated :py:class:`model.Key`
            objects. '''

        pass

    @rpc.method(messages.EventRange, messages.Events)
    def get_range(self, request):

        ''' Retrieve a range of :py:class:`event.TrackedEvent`
            models by special values attached to them. '''

        pass
