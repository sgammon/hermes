# -*- coding: utf-8 -*-

'''
The :py:class:`EventStorage` class handles calls to
underlying storage mechanisms.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Platform Parent
from api.platform import PlatformBridge

# Model Adapters
from apptools.model.adapter import redis
from apptools.model.adapter import inmemory


## EventStorage - handles low-level storage calls.
class EventStorage(PlatformBridge):

    ''' Handles datastore integration and
        propagation of data to underlying
        storage mechanisms. '''

    ## DatastoreEngine - static, encapsulated adapter import.
    class DatastoreEngine(object):

        ''' Encapsulated attachment of symbols to
            :py:mod:`model.adapter.redis` and
            :py:mod:`model.adapter.inmemory`. '''

        redis = redis.RedisAdapter
        memory = inmemory.InMemoryAdapter
