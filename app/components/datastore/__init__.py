# -*- coding: utf-8 -*-

'''

Components: Datastore

This component holds a `DatastoreEngine` actor that wakes
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

    __version__ = (0, 2)  # current engine version

    socket = None  # active socket to redis
    tracker = None  # reference to the `EventTracker` server
    inflight = None  # holds inflight requests in non-pipelined mode

    class EngineConfig(object):

        ''' Configuration values for the `DatastoreEngine`. '''

        pipeline = True  # enable pipelined redis commands
        transactional = False  # commit data transactionally

    class Operations(object):

        ''' Available datastore operations. '''

        ## Key Operations
        SET = 'SET'  # set a value at a key directly
        GET = 'GET'  # get a value by key directly
        KEYS = 'KEYS'  # get a list of all keys matching a regex
        DUMP = 'DUMP'  # dump serialized information about a key
        DELETE = 'DEL'  # delete a key=> value pair, by key
        GETSET = 'GETSET'  # set a value by key, and return the existing value at that key

        ## Counter Operations
        INCREMENT = 'INCR'  # increment a key (`str` or `int`) by 1
        DECREMENT = 'DECR'  # decrement a key (`str` or `int`) by 1
        INCREMENT_BY = 'INCRBY'  # increment a key (`str` or `int`) by X
        DECREMENT_BY = 'DECRBY'  # decrement a key (`str` or `int`) by X

        ## Hash Operations
        HASH_SET = 'HSET'  # set the value of an individual hash field
        HASH_GET = 'HGET'  # get the value of an individual hash field
        HASH_DELETE = 'HDEL'  # delete one or more individual hash fields
        HASH_LENGTH = 'HLEN'  # retrieve the number of fields in a hash
        HASH_VALUES = 'HVALS'  # get all values in a hash, without keys
        HASH_EXISTS = 'HEXISTS'  # determine if an individual hash field exists
        HASH_MULTI_GET = 'HMGET'  # get the values of multiple hash fields
        HASH_MULTI_SET = 'HMSET'  # set the values of multiple hash fields
        HASH_INCREMENT = 'HINCRBY'  # increment an individual hash field by X

        ## String Commands
        APPEND = 'APPEND'  # append string data to to an existing key
        STRING_LENGTH = 'STRLEN'  # retrieve the length of a string value at a key

        ## List Operations
        LIST_SET = 'LSET'  # set a value in a list by its index
        LEFT_POP = 'LPOP'  # pop a value off the left side of a list
        RIGHT_POP = 'RPOP'  # pop a value off the right side of a list
        LEFT_PUSH = 'LPUSH'  # add a value to the right side of a list
        RIGHT_PUSH = 'RPUSH'  # add a value to the right side of a list
        LEFT_PUSH_X = 'LPUSHX'  # add a value to the left side of a list, only if it already exists
        RIGHT_PUSH_X = 'RPUSHX'  # add a value to the right side of a list, only if it already exists
        LIST_TRIM = 'LTRIM'  # truncate the list to only containing X values
        LIST_INDEX = 'LINDEX'  # get a value from a list by its index
        LIST_RANGE = 'LRANGE'  # get a range of values from a list
        LIST_LENGTH = 'LLEN'  # retrieve the current length of a list
        LIST_REMOVE = 'LREM'  # remove elements from an existing list
        BLOCK_LEFT_POP = 'BLPOP'  # same as lpop, but block until an item is available
        BLOCK_RIGHT_POP = 'BRPOP'  # same as rpop, but block until an item is available

        ## Set Operations
        SET_ADD = 'SADD'  # add a new member to a set
        SET_POP = 'SPOP'  # pop and remove an item from the end of a set
        SET_MOVE = 'SMOVE'  # move a member from one set to another
        SET_DIFF = 'SDIFF'  # calculate the difference/delta of two sets
        SET_UNION = 'SUNION'  # calculate the union/combination of two sets
        SET_REMOVE = 'SREM'  # remove one or more members from a set
        SET_MEMBERS = 'SMEMBERS'  # retrieve all members of a set
        SET_INTERSECT = 'SINTER'  # calculate the intersection of two sets
        SET_IS_MEMBER = 'SISMEMBER'  # determine if a value is a member of a set
        SET_DIFF_STORE = 'SDIFFSTORE'  # calculate the delta of two sets and store the result
        SET_CARDINALITY = 'SCARD'  # calculate the number of members in a set
        SET_UNION_STORE = 'SUNIONSTORE'  # calculate the union of two sets and store the result
        SET_RANDOM_MEMBER = 'SRANDMEMBER'  # retrieve a random member of a set
        SET_INTERSECT_STORE = 'SINTERSTORE'  # calculate the intersection of a set and store the result

        ## Sorted Set Operations
        SORTED_ADD = 'ZADD'  # add a member to a sorted set
        SORTED_RANK = 'ZRANK'  # determine the index o a member in a sorted set
        SORTED_RANGE = 'ZRANGE'  # return a range of members in a sorted set, by index
        SORTED_SCORE = 'ZSCORE'  # get the score associated with the given member in a sorted set
        SORTED_COUNT = 'ZCOUNT'  # count the members in a sorted set with scores within a given range
        SORTED_REMOVE = 'ZREM'  # remove one or more members from a sorted set
        SORTED_CARDINALITY = 'ZCARD'  # get the number of members in a sorted set (cardinality)
        SORTED_UNION_STORE = 'ZUNIONSTORE'  # compute the union of two sorted sets, storing the result at a new key
        SORTED_INCREMENT_BY = 'ZINCRBY'  # increment the score of a member in a sorted set by X
        SORTED_INDEX_BY_SCORE = 'ZREVRANK'  # determine the index of a member in a sorted set, with scores ordered high=>low
        SORTED_RANGE_BY_SCORE = 'ZRANGEBYSCORE'  # return a range of members in a sorted set, by score
        SORTED_INTERSECT_STORE = 'ZINTERSTORE'  # intersect multiple sets, storing the result in a new key
        SORTED_MEMBERS_BY_INDEX = 'ZREVRANGE'  # return a range of members in a sorted set, by index, scores ordered high=>low
        SORTED_MEMBERS_BY_SCORE = 'ZREVRANGEBYSCORE'  # remove all members in a sorted set within the given scores
        SORTED_REMOVE_RANGE_BY_RANK = 'ZREMRANGEBYRANK'  # remove members in a sorted set within a given range of ranks
        SORTED_REMOVE_RANGE_BY_SCORE = 'ZREMRANGEBYSCORE'  # remove members in a sorted set within a given range of scores

        ## Pub/Sub Operations
        PUBLISH = 'PUBLISH'  # publish a message to a specific pub/sub channel
        SUBSCRIBE = 'SUBSCRIBE'  # subscribe to messages on an exact channel
        UNSUBSCRIBE = 'UNSUBSCRIBE'  # unsubscribe from messages on an exact channel
        PATTERN_SUBSCRIBE = 'PSUBSCRIBE'  # subscribe to all pub/sub channels matching a pattern
        PATTERN_UNSUBSCRIBE = 'PUNSUBSCRIBE'  # unsubscribe from all pub/sub channels matching a pattern

        ## Transactional Operations
        EXEC = 'EXEC'  # execute buffered commands in a pipeline queue
        MULTI = 'MULTI'  # start a new pipeline, where commands can be buffered
        WATCH = 'WATCH'  # watch a key, such that we can receive a notification in the event it is modified while watching
        UNWATCH = 'UNWATCH'  # unwatch all currently watched keys
        DISCARD = 'DISCARD'  # discard buffered commands in a pipeline completely

        ## Scripting Operations
        EVALUATE = 'EVAL'  # evaluate a script inline, written in Lua
        EVALUATE_STORED = 'EVALSHA'  # execute an already-loaded script
        SCRIPT_LOAD = 'SCRIPT LOAD'  # load a script into memory for future execution
        SCRIPT_KILL = 'SCRIPT KILL'  # kill the currently running script
        SCRIPT_FLUSH = 'SCRIPT FLUSH'  # flush all scripts from the script cache
        SCRIPT_EXISTS = 'SCRIPT EXISTS'  # check existence of scripts in the script cache

        ## Connection Operations
        ECHO = 'ECHO'  # echo the given string from the server side - for testing
        PING = 'PING'  # 'ping' to receive a 'pong' from the server - for keepalive
        QUIT = 'QUIT'  # exit and close the current connection
        SELECT = 'SELECT'  # select the currently-active database
        AUTHENTICATE = 'AUTH'  # authenticate to a protected redis instance

        ## Server Operations
        TIME = 'TIME'  # get the current time, as seen by the server
        SYNC = 'SYNC'  # internal command - for master/slave propagation
        SAVE = 'SAVE'  # synchronously save the dataset to disk
        INFO = 'INFO'  # get information and statistics about the server
        DEBUG = 'DEBUG OBJECT'  # get detailed debug information about an object
        DB_SIZE = 'DBSIZE'  # get the number of keys in a database
        SLOWLOG = 'SLOWLOG'  # manages the redis slow queries log
        MONITOR = 'MONITOR'  # listen for all requests received by the server in realtime
        SLAVE_OF = 'SLAVEOF'  # make the server a slave, or promote it to master
        SHUTDOWN = 'SHUTDOWN'  # synchronously save to disk and shutdown the server process
        FLUSH_DB = 'FLUSHDB'  # flush all keys and values from the current database
        FLUSH_ALL = 'FLUSHALL'  # flush all keys and values in all of redis
        LAST_SAVE = 'LASTSAVE'  # retrieve a UNIX timestamp indicating the last successful save to disk
        CONFIG_GET = 'CONFIG GET'  # get the value of a redis configuration parameter
        CONFIG_SET = 'CONFIG SET'  # set the value of a redis configuration parameter
        CLIENT_KILL = 'CLIENT KILL'  # kill a client's active connection with redis
        CLIENT_LIST = 'CLIENT LIST'  # list all the active client connctions with redis
        CLIENT_GET_NAME = 'CLIENT GETNAME'  # get the name of the current connection
        CLIENT_SET_NAME = 'CLIENT SETNAME'  # set the name of the current connection
        CONFIG_RESET_STAT = 'CONFIG RESETSTAT'  # reset infostats that are served by "INFO"
        BACKGROUND_SAVE = 'BGSAVE'  # in the background, save the current dataset to disk
        BACKGROUND_REWRITE = 'BGREWRITEAOF'  # in the background, rewrite the current AOF

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
