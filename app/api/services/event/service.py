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


## EventDataService - exposes methods for extracting data from `EventTracker`.
@rpc.service
class EventDataService(rpc.Service):

    ''' Exposes methods for interacting with & extracting data from `EventTracker`. '''

    _config_path = 'hermes.api.tracker.EventDataAPI'

    exceptions = rpc.Exceptions(**{
        'generic': exceptions.Error
    })

    pass
