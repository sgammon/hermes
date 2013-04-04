# -*- coding: utf-8 -*-

'''

Components: Datastore

This components holds a `DatastoreEngine` actor that wakes
up and writes `TrackedEvent`(s) to Redis. This engine
supports command pipelining and configurable autobatching.

-sam (<sam.gammon@ampush.com>)

'''

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
from config import debug
from config import verbose
from config import _REDIS_DB
from config import _REDIS_SOCK
from config import _REDIS_WRITE_POOL
from config import _RUNTIME_SOCKROOT


## Globals / Monkeypatching
redis.connection.socket = gevent.socket

## Global Pools
_write_pool = pool.Pool(_REDIS_WRITE_POOL)
_sock = '/'.join([_RUNTIME_SOCKROOT, _REDIS_SOCK])

## Redis Client
client = redis.StrictRedis(unix_socket_path=_sock, db=_REDIS_DB)
_connection_pool = client.connection_pool


## DatastoreEngine - manages cooperative writes to a given backend
class DatastoreEngine(actor.Actor):

	''' Datastore adapter and transaction engine. '''

	socket = None
	tracker = None
	inflight = None

	class EngineConfig(object):

		''' Configuration values for the `DatastoreEngine`. '''

		pipeline = True
		transactional = False

	class Operations(object):

		''' Available datastore operations. '''

		SET = 'set'
		GET = 'get'
		INCR = 'incr'
		HSET = 'hset'

	def __init__(self, tracker, redis=_sock):

		''' Initialize this DatastoreEngine. '''

		self.tracker, self.socket = tracker, redis
		if debug:
			self.log("Datastore: Initialized datastore engine.")
			self.verbose("Datastore: Connecting to Redis at %s." % redis)
			self.verbose("Datastore: Connection pool limited to %s." % _REDIS_WRITE_POOL)
		self.initialize().start()

	@property
	def writepool(self):

		''' Retrieve the global writepool. '''

		global _write_pool
		return _write_pool

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

	def _write_item(self, item):

		''' Write a single item. '''
		
		if verbose:
			self.verbose("Datastore: Executing operation %s." % str(item))

		try:
			## Execute queued command, optionally with args
			if len(item) > 1:
				result = getattr(self.redis, item[0])(*item[1:])
			else:
				result = getattr(self.redis, item[0])()

		except Exception as e:
			self.error("Datastore: Encountered UNHANDLED WRITE EXCEPTION %s! Data was lost!" % e)
			raise

		return result

	def _write_batch(self, batch):

		''' Write a batch of items. '''

		pipeline = client.pipeline(transaction=self.EngineConfig.transactional)
		self.log("Datastore: Opened new pipeline with ID %s (transactions are %s)." % (id(pipeline), "ON" if self.EngineConfig.transactional else "OFF"))

		## Put in multi-mode
		pipeline.multi()
		for op in batch:

			# Queue up the writes in the pipeline buffer
			self.verbose("Datastore: Enqueueing operation %s." % str(op))
			if len(op) > 1:
				getattr(pipeline, op[0])(*op[1:])
			else:
				getattr(pipeline, op[0])()

		## Execute pipeline
		self.verbose("Datastore: Executing pipeline...")
		start_timestamp = time.time()
		result = pipeline.execute()

		## Log result
		finish_timestamp = time.time()
		self.log("Datastore: Finished pipeline execution in %s seconds." % (finish_timestamp - start_timestamp))
		self.verbose("Datastore: Pipeline result == \"%s\"." % str(result))

		return result

	def execute(self, operations):

		''' Perform a write operation against Redis. '''

		## If pipelined, spawn new pipeline greenlet
		if self.EngineConfig.pipeline:
			writethread = gevent.spawn(self._write_batch, operations)
			gevent.sleep(0)
			return self

		else:
			if self.inflight:
				## Reap previous writelets
				self.verbose("Datastore: Reaping %s previous inflight writes." % len(self.inflight))
				gevent.joinall(self.inflight)

			self.inflight = [g for g in self.writepool.map_async(self._write_item, operations)]
			self.verbose("Datastore: Spawned %s inflight writes." % len(self.inflight))
			gevent.sleep(0)
			return self

	def serialize(self, deque):

		''' Serialize a single operation into an appropriate Redis call. '''

		_write_queue = []
		for event in deque:
			objects, indexes = event.serialize()
			for key, obj in objects.items():
				_write_queue.append((self.Operations.SET, key, json.dumps(obj)))

		self.verbose('Datastore: Generated writequeue of length %s.' % len(_write_queue))
		return _write_queue

	def fire(self, operation, autobatch=True):

		''' Execution entrypoint for a queued item. '''

		self.log("Datastore: Firing on ready buffered frame %s." % id(operation))
		return self.execute(self.serialize(operation))
