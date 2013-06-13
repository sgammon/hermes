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


## Profile
class Profile(rpc.messages.Message):

    ''' Expresses an individual descendent of
        :py:class:`policy.core.Profile`. '''

    pass


## Profiles
class Profiles(rpc.messages.Message):

    ''' Expresses a set of all (or 'matching')
        :py:class:`policy.core.Profile` descendents. '''

    pass


## ProvisioningRequest
class ProvisioningRequest(rpc.messages.Message):

    ''' Expresses a request to provision (create)
        one (or multiple) :py:class:`endpoint.Tracker`
        model(s). '''

    pass


## TrackerSet
class TrackerSet(rpc.messages.Message):

    ''' Expresses a set of :py:class:`endpoint.Tracker`
        objects. '''

    pass
