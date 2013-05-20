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

# tools
from tools import actor

# constants
from config import debug


## DatastoreEngine - manages cooperative writes to a given backend
class DatastoreEngine(actor.Actor):

    ''' Datastore adapter and transaction engine. '''

    __version__ = (0, 3)  # current engine version

    tracker = None  # reference to the `EventTracker` server
    inflight = None  # holds inflight requests in non-pipelined mode

    def __init__(self, tracker):

        ''' Initialize this DatastoreEngine. '''

        self.tracker = tracker
        self.log("Datastore: Initialized datastore engine.")
        self.initialize().start()

    if debug:
        @property
        def log(self):

            ''' Log to the current tracker. '''

            return self.tracker.log

        @property
        def verbose(self):

            ''' Log verbosely to the current tracker. '''

            return self.tracker.verbose


    else:
        @property
        def log(self):

            ''' Log blackhole. '''

            def blackhole(*args, **kwargs):
                return self

        @property
        def verbose(self):

            ''' Soak up any verbose logs to the current tracker. '''

            def blackhole(*args, **kwargs):
                return self

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

        '''
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
        '''
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

        self.log("Datastore: Firing on buffered frame %s." % id(operation))
        #return self.execute(self.serialize(operation))
