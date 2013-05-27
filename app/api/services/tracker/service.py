# -*- coding: utf-8 -*-

'''
Tracker API: Service

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Local Imports
from . import messages
from . import exceptions

# apptools rpc + model
from apptools import rpc
from apptools import model

# API Service
from api.services import APIService


## Echo
# Sample message.
class Echo(model.Model):

    ''' Sample model => message. '''

    message = basestring, {'default': 'Hello, world!'}


## TrackerService - exposes methods for managing config for `EventTracker`.
@rpc.service
class TrackerService(APIService):

    ''' Exposes methods for managing the `EventTracker`. '''

    _config_path = 'hermes.api.tracker.TrackerAPI'

    exceptions = rpc.Exceptions(**{
        'generic': exceptions.Error
    })

    @rpc.method(Echo, Echo)
    def echo(self, request):

        ''' Echo back what we get. '''

        if request.message:
            return Echo(message=request.message)
        return Echo()
