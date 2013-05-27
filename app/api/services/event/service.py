# -*- coding: utf-8 -*-

'''
Event Data API: Service

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Local Imports
from . import exceptions

# apptools rpc
from apptools import rpc

# apptools util
from apptools.util import datastructures

# API Service
from api.services import APIService


## EventDataService - exposes methods for extracting data from `EventTracker`.
@rpc.service
class EventDataService(APIService):

    ''' Exposes methods for interacting with & extracting data from `EventTracker`. '''

    _config_path = 'hermes.api.tracker.EventDataAPI'

    exceptions = datastructures.DictProxy(**{
        'generic': exceptions.Error
    })

    pass
