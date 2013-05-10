# -*- coding: utf-8 -*-

'''

Raw Data API: Service

-sam (<sam.gammon@ampush.com>)

'''

# Base Imports
import config
import webapp2

# Local Imports
from . import messages
from . import exceptions

# apptools services
from apptools import services

# apptools util
from apptools.util import debug
from apptools.util import datastructures

# API Service
from api.services import APIService


## RawDataService - exposes methods for retrieving raw data from `EventTracker`.
class RawDataService(APIService):

    ''' Exposes methods for retrieving raw data from `EventTracker`. '''

    _config_path = 'hermes.api.tracker.RawDataAPI'

    exceptions = datastructures.DictProxy(**{
        'generic': exceptions.Error
    })

    @webapp2.cached_property
    def config(self):

        ''' Cached access to `RawDataService` config. '''

        return config.config.get(self._config_path, {'debug': False})

    @webapp2.cached_property
    def logging(self):

        ''' Cached access to dedicated log pipe. '''

        path = self._config_path.split('.')
        return debug.AppToolsLogger(path='.'.join(path[0:-1]), name=path[-1])._setcondition(self.config.get('debug'))
