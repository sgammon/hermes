# -*- coding: utf-8 -*-

'''
Tracker API: Messages

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# RPC API
from apptools import rpc

# Endpoint Models
from api.models.tracker import endpoint


## Profile - expresses a single descendent of :py:class:`policy.core.Profile`.
class Profile(rpc.messages.Message):

    ''' Expresses an individual descendent of
        :py:class:`policy.core.Profile`. '''

    pass


## Profiles - expresses a collection of :py:class:`Profile` entities.
class Profiles(rpc.messages.Message):

    ''' Expresses a set of all (or 'matching')
        :py:class:`policy.core.Profile` descendents. '''

    pass


## ProvisioningRequest - expresses a request to provision one or multiple :py:class:`Tracker` entities.
class ProvisioningRequest(rpc.messages.Message):

    ''' Expresses a request to provision (create)
        one (or multiple) :py:class:`endpoint.Tracker`
        model(s). '''

    owner = rpc.messages.StringField(1, required=True)
    spec = rpc.messages.MessageField(endpoint.Tracker.to_message_model(), 2)
    specs = rpc.messages.MessageField(endpoint.Tracker.to_message_model(), 3, repeated=True)


## TrackerSet - expresses a collection of :py:class:`Tracker` entities.
class TrackerSet(rpc.messages.Message):

    ''' Expresses a set of :py:class:`endpoint.Tracker`
        objects. '''

    count = rpc.messages.IntegerField(1, default=0)
    trackers = rpc.messages.MessageField(endpoint.Tracker.to_message_model(), 3, repeated=True)
