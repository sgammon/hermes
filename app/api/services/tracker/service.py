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

# Endpoint Models
from api.models.tracker import endpoint


## TrackerService - exposes methods for managing config for `EventTracker`.
@rpc.service
class TrackerService(rpc.Service):

    ''' Exposes methods for managing the `EventTracker`. '''

    _config_path = 'hermes.api.tracker.TrackerAPI'

    exceptions = rpc.Exceptions(**{
        'generic': exceptions.Error,
        'tracker_not_found': exceptions.TrackerNotFound
    })

    @rpc.method(model.Key, endpoint.Tracker)
    def get(self, request):

        ''' Retrieve a :py:class:`Tracker` by ID or its associated
            :py:class:`model.Key`.

            :param request: Accepts a full or partial :py:class:`model.Key`.
            :raises TrackerNotFound:
            :returns: '''

        pass

    @rpc.method(endpoint.Tracker)
    def put(self, request):

        ''' Low-level method to persist a :py:class:`Tracker` model.
            Usually used for saving updates to existing ``Tracker``
            entities.

            :param request:
            :raises:
            :returns: '''

        pass

    @rpc.method(messages.Profiles)
    def profiles(self, request):

        ''' Retrieves available/configured :py:class:`Profile`
            descendents that may be used via :py:meth:`provision`
            or any other place that requires an ``EventProfile``.

            :param request:
            :raises:
            :returns: '''

        pass

    @rpc.method(messages.ProvisioningRequest, messages.TrackerSet)
    def provision(self, request):

        ''' Provision a single :py:class:`Tracker`, according
            to the given spec in :py:class:`ProvisionRequest`.

            :param request:
            :raises:
            :returns: '''

        pass
