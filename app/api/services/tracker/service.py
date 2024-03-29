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

    ''' Exposes methods for configuring the ``EventTracker``, including
        the creation/management of :py:class:`Tracker` objects, the
        retrieval of runtime statistics, and other platform-wide utils. '''

    name = 'tracker'
    _config_path = 'hermes.api.tracker.TrackerAPI'

    exceptions = rpc.Exceptions(**{
        'generic': exceptions.Error,
        'tracker_not_found': exceptions.TrackerNotFound,
        'provision_failed': exceptions.ProvisionFailed
    })

    @rpc.method(model.Key, endpoint.Tracker)
    def get(self, request):

        ''' Retrieve a :py:class:`Tracker` by ID or its associated
            :py:class:`model.Key`.

            :param request: Accepts a full or partial :py:class:`model.Key`.
            :raises TrackerNotFound:
            :returns: '''

        raise self.exceptions.generic('Service method `get` is currently stubbed.')

    @rpc.method(endpoint.Tracker)
    def put(self, request):

        ''' Low-level method to persist a :py:class:`Tracker` model.
            Usually used for saving updates to existing ``Tracker``
            entities.

            :param request:
            :raises:
            :returns: '''

        raise self.exceptions.generic('Service method `put` is currently stubbed.')

    @rpc.method(messages.Profile)
    def profile(self, request):

        ''' Retrieves a single :py:class:`Profile` class
            descendent, via a fully-qualified path,
            ``refname`` value, :py:class:`raw.Event` key
            or :py:class:`event.TrackedEvent` key.

            :param request:
            :raises:
            :returns: '''

        raise self.exceptions.generic('Service method `profile` is currently stubbed.')

    @rpc.method(messages.Profiles)
    def profiles(self, request):

        ''' Retrieves available/configured :py:class:`Profile`
            descendents that may be used via :py:meth:`provision`
            or any other place that requires an ``EventProfile``.

            :param request:
            :raises:
            :returns: '''

        raise self.exceptions.generic('Service method `profiles` is currently stubbed.')

    @rpc.method(messages.ProvisioningRequest, messages.TrackerSet)
    def provision(self, request):

        ''' Provision a single :py:class:`Tracker`, according
            to the given spec in :py:class:`ProvisionRequest`.

            :param request:
            :raises:
            :returns: '''

        try:

            # build a single tracker
            if request.spec:

                return messages.TrackerSet(**{
                    'count': 1,
                    'trackers': [
                        self.tracker.provision(request.owner, spec=request.spec).to_message()
                    ]
                })

            # build multiple trackers
            if request.specs:

                # build trackers
                trackers = self.tracker.provision(request.owner, specs=request.specs)

                # provision trackers
                return messages.TrackerSet(**{
                    'count': len(trackers),
                    'trackers': map(lambda x: x.to_message(), trackers)
                })

            else:
                raise self.exceptions.provision_failed('Must provide parameter `spec` or `specs`.')

        except Exception as e:
            context = (e.__class__.__name__, str(e))
            raise self.exceptions.provision_failed('Request to provision failed with '
                                                   'exception: "%s". Message: "%s".' % context)
