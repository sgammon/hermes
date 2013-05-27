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

# apptools util
from apptools.util import datastructures

# API Service
from api.services import APIService


## RawDataService - exposes methods for retrieving raw data from `EventTracker`.
@rpc.service
class RawDataService(APIService):

    ''' Exposes methods for retrieving raw data from `EventTracker`. '''

    _config_path = 'hermes.api.tracker.RawDataAPI'

    exceptions = datastructures.DictProxy(**{
        'generic': exceptions.Error
    })

    pass
