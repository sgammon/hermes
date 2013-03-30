# -*- coding: utf-8 -*-

# stdlib
import time
import json

# gevent
import gevent
from gevent import pool
from gevent import queue

# redis
import redis
import redis.connection

# tools
from tools import actor

# constants
from config import _REDIS_DB
from config import _REDIS_SOCK
from config import _REDIS_WRITE_POOL
from config import _RUNTIME_SOCKROOT


## Globals / Monkeypatching
redis.connection.socket = gevent.socket

## Global Pools
_write_pool = pool.Pool(_REDIS_WRITE_POOL)
_sock = '/'.join([_RUNTIME_SOCKROOT, _REDIS_SOCK])
_connection_pool = redis.ConnectionPool(unix_socket_path=_sock, db=_REDIS_DB)

## Redis Client
client = redis.StrictRedis(connection_pool=_connection_pool)


## DatastoreEngine - manages cooperative writes to a given backend
class DatastoreEngine(actor.Actor):

	''' Datastore adapter and transaction engine. '''

	socket = None
	tracker = None

	def __init__(self, tracker, redis=_sock):

		''' Initialize this DatastoreEngine. '''

		self.tracker, self.socket = tracker, redis
		self.log("Datastore: Initialized datastore engine.")
		self.verbose("Datastore: Connecting to Redis at %s." % redis)
		self.verbose("Datastore: Connection pool limited to %s." % _REDIS_WRITE_POOL)
		self.initialize().start()

	@property
	def writepool(self):

		''' Retrieve the global writepool. '''

		global _writepool
		return _writepool

	@property
	def redis(self):

		''' Retrieve the current Redis connection object. '''

		global client
		return client

	@property
	def log(self):

		''' Log to the current tracker. '''

		return self.tracker.log

	@property
	def verbose(self):

		''' Verbose-log to the current tracker. '''

		return self.tracker.verbose

	@property
	def warn(self):

		''' Warn to the current tracker. '''

		return self.tracker.warn

	@property
	def error(self):

		''' Err to the current tracker. '''

		return self.tracker.error

	def execute(self, operations):

		''' Perform a write operation against Redis. '''

		for op in operations:
			print "= !! WOULD EXECUTE: %s !! ==" % str(op)

		time.sleep(0.1)
		return self

	def serialize(self, deque):

		''' Serialize a single operation into an appropriate Redis call. '''

		_write_queue = []
		for event in deque:
			objects, indexes = event.serialize()
			for key, obj in objects.items():
				_write_queue.append((self.redis.set, key, json.dumps(obj)))

		self.verbose('Datastore: Generated writequeue of length %s.' % len(_write_queue))
		return _write_queue

	def fire(self, operation, autobatch=True):

		''' Execution entrypoint for a queued item. '''

		self.log("Datastore: Firing on ready buffered frame %s." % id(operation))
		return self.execute(self.serialize(operation))