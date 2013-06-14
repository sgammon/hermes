# -*- coding: utf-8 -*-

'''
This package holds classes that describe data structures. Expressing a data
structure as a model allows use of hot-pluggable persistence and caching
backends, among other handy bridges. apptools models can quickly be
converted to ProtoRPC messages, JSON structures, dictionaries, and more.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# stdlib
import datetime

# apptools model
from apptools import model


## Test for Redis support
try:
    import redis; _REDIS = True
except ImportError:  # pragma: no cover
    _REDIS = False


## TrackerModel
# Abstract parent for all `EventTracker` models.
class TrackerModel(model.Model):

    ''' Abstract parent for all `EventTracker` models. '''

    __adapter__ = "RedisAdapter" if _REDIS else "InMemoryAdapter"

    # == Timestamps == #
    modified = datetime.datetime, {'auto_now': True}  # timestamp for when this was last modified
    created = datetime.datetime, {'auto_now_add': True}  # timestamp for when this was first saved
