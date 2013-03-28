# -*- coding: utf-8 -*-

# gevent
import gevent
from gevent import pool

# contants
from apps.hermes.source import _REDIS_WRITE_POOL


## Globals
_writepool = pool.Pool(_REDIS_WRITE_POOL)


## DatastoreEngine - manages cooperative writes to a given backend
class DatastoreEngine(object):

	''' Datastore adapter and transaction engine. '''

	pass
