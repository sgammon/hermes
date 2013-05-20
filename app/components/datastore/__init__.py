# -*- coding: utf-8 -*-

'''
Components: Datastore

This component holds a `DatastoreEngine` actor that wakes
up and writes `TrackedEvent`(s) to Redis. This engine
supports command pipelining and configurable autobatching.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
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

        ''' Initialize this DatastoreEngine.
            :param tracker: The current :py:class:`EventTracker` server. '''

        self.tracker = tracker
        self.log("Datastore: Initialized datastore engine.")
        self.initialize().start()

    if debug:
        @property
        def log(self):

            ''' Log to the current tracker.
                :returns: Active logger on :py:class:`EventTracker`. '''

            return self.tracker.log

        @property
        def verbose(self):

            ''' Log verbosely to the current tracker.
                :returns: Active verbose logger on :py:class:`EventTracker`. '''

            return self.tracker.verbose


    else:
        @property
        def log(self):

            ''' Log blackhole.

                :param args: Arguments to be discarded.
                :param kwargs: Keyword arguments to be discarded.
                :returns: Self, for chainability. '''

            def blackhole(*args, **kwargs):
                return self

        @property
        def verbose(self):

            ''' Soak up any verbose logs to the current tracker.

                :param args: Arguments to be discarded.
                :param kwargs: Keyword arguments to be discarded.
                :returns: Self, for chainability. '''

            def blackhole(*args, **kwargs):
                return self

    @property
    def warn(self):

        ''' Warn to the current tracker.
            :returns: Self, for chainaibility. '''

        return self.tracker.warn

    @property
    def error(self):

        ''' Err to the current tracker.
            :returns: Error logger on :py:class:`EventTracker`. '''

        return self.tracker.error

    def _write_item(self, item):

        ''' Write a single item to Redis.

            :param item: The write bundle to commit to Redis.
            :returns: The result of the write call. '''

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

        ''' Write a batch of items.

            :param batch: The batch of write bundles to commit to Redis.
            :returns: The result of the committed pipeline. '''

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

        ''' Perform a write operation against Redis.

            :param operations: Bundle of pre-processed write operations.
            :returns: Self, for chainability. '''

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

        ''' Serialize a single operation into an appropriate Redis call.

            :param deque: :py:class:`TrackedEvent` records due for serialization.
            :returns: Serialized queue of writes for the items in ``deque``. '''

        _write_queue = []
        for event in deque:
            objects, indexes = event.serialize()
            for key, obj in objects.items():
                _write_queue.append((self.Operations.SET, key, json.dumps(obj)))

        self.verbose('Datastore: Generated writequeue of length %s.' % len(_write_queue))
        return _write_queue

    def fire(self, operation, autobatch=True):

        ''' Execution entrypoint for a queued item.

            :param operation: Operation object, describing what the engine should do.
            :param autobatch: Boolean, defaults to ``True``. Activates the autobatcher.
            :returns: Nothing, as we are working across :py:class:`gevent.Greenlet` bounds here. '''

        self.log("Datastore: Firing on buffered frame %s." % id(operation))
        #return self.execute(self.serialize(operation))
