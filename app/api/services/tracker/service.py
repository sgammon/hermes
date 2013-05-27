# -*- coding: utf-8 -*-

'''
Tracker API: Service

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

# protorpc
from protorpc import remote

# apptools services
from apptools import model
from apptools import services

# apptools util
from apptools.util import debug
from apptools.util import datastructures

# API Service
from api.services import APIService


## Echo
# Sample message.
class Echo(model.Model):

    ''' Sample model => message. '''

    message = basestring, {'default': 'Hello, world!'}


Echo = Echo.to_message_model()


## TrackerService - exposes methods for managing config for `EventTracker`.
class TrackerService(APIService):

    ''' Exposes methods for managing the `EventTracker`. '''

    _config_path = 'hermes.api.tracker.TrackerAPI'

    exceptions = datastructures.DictProxy(**{
        'generic': exceptions.Error
    })

    @remote.method(Echo, Echo)
    def echo(self, request):

        ''' Echo back what we get. '''

        if request.message:
            return Echo(message=request.message)
        return Echo()
