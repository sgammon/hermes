# -*- coding: utf-8 -*-

'''
Event Data API: Service

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
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


## EventDataService - exposes methods for extracting data from `EventTracker`.
class EventDataService(APIService):

    ''' Exposes methods for interacting with & extracting data from `EventTracker`. '''

    _config_path = 'hermes.api.tracker.EventDataAPI'

    exceptions = datastructures.DictProxy(**{
        'generic': exceptions.Error
    })

    @webapp2.cached_property
    def config(self):

        ''' Cached access to `EventDataService` config. '''

        return config.config.get(self._config_path, {'debug': False})

    @webapp2.cached_property
    def logging(self):

        ''' Cached access to dedicated log pipe. '''

        path = self._config_path.split('.')
        return debug.AppToolsLogger(path='.'.join(path[0:-1]), name=path[-1])._setcondition(self.config.get('debug'))
