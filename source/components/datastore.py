# -*- coding: utf-8 -*-

# gevent
import gevent
from gevent import pool

# redis
import redis
import redis.connection

# contants
from apps.hermes.source import _REDIS_WRITE_POOL
from apps.hermes.source import _RUNTIME_SOCKROOT


## Globals / Monkeypatching
client = redis.StrictRedis()
redis.connection.socket = gevent.socket

## Global Pools
_write_pool = pool.Pool(_REDIS_WRITE_POOL)
_connection_pool = client.connection_pool


## DatastoreConnection - provisioned and leased according to _writepool
class DatastoreConnection(object):

	''' Connection wrapper to Redis. '''

	id = None  # numeric index of connection, for logging/synchronization
	socket = None  # unix domain socket (string) or TCP/IP socket (tuple) for redis communications
	_transport = None  # private property with gevent-redis connection object

	@classmethod
	def provision(cls, engine, redis, i):

		''' Provision a new DatastoreConnection. '''

		return cls(id=i, engine=engine, socket=redis)

	def __init__(self, **kwargs):

		''' Initialize this DatastoreConnection. '''

		for k, v in kwargs.items():
			setattr(self, k, v)

	@property
	def transport(self):

		''' Establish or resume an active Redis connection. '''

		connection = 


## DatastoreEngine - manages cooperative writes to a given backend
class DatastoreEngine(object):

	''' Datastore adapter and transaction engine. '''

	connections = None  # holds a bounded number of datastore connections

	def __init__(self, tracker, redis='/'.join([_RUNTIME_SOCKROOT, 'redis.sock'])):

		''' Initialize this DatastoreEngine. '''

		self.connections = []
		for i in xrange(0, _REDIS_WRITE_POOL):
			self.connections.append(DatastoreConnection.provision(self, redis, i))

	@property
	def writepool(self):

		''' Retrieve the global writepool. '''

		global _writepool
		return _writepool
