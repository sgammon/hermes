# -*- coding: utf-8 -*-

'''
The :py:class:`EventEngine` class handles calls to
underlying storage mechanisms.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# apptools util
import logging

# Platform Parent
from api.platform import PlatformBridge

# apptools util
from apptools.util import datastructures

# Model Adapters
from apptools.model.adapter import redis
from apptools.model.adapter import inmemory

# detect redis support
try:
    from redis import client; _REDIS = True
except ImportError:
    _REDIS = False
    logging.warning('Redis not found. Tracker engine falling back to `InMemory` storage - pubsub will be unavailable.')


# Globals
_connection = None


## EventEngine - handles low-level propagation and IO.
class EventEngine(PlatformBridge):

    ''' Handles datastore integration and
        propagation of data to underlying
        storage mechanisms. '''

    ## Datastore - static, encapsulated adapter import.
    class Datastore(object):

        ''' Encapsulated attachment of symbols to
            :py:mod:`model.adapter.redis` and
            :py:mod:`model.adapter.inmemory`. '''

        redis = redis.RedisAdapter
        memory = inmemory.InMemoryAdapter

    redis = datastructures.DictProxy(**{

        'Operations': Datastore.redis.Operations,
        'EngineConfig': Datastore.redis.EngineConfig

    })

    ## === Internal Methods === ##
    def _spawn(self, func, *args, **kwargs):

        ''' Spawn a new ``Greenlet`` encapsulating an
            :py:class:`EventStorage` operation. This
            method is used internally to spawn and
            schedule ``Greenlets``.

            :param func: Callable to wrap in a ``Greenlet``.
            :param *args: Positional arguments to pass to the callable.
            :param **kwargs: Keyword arguments to pass to the callable.
            :returns: A new ``Greenlet``, which is ready to schedule for
            coopperative execution. '''

        raise NotImplementedError('Method `_spawn` is not yet supported.')

    ## === Bindings === ##
    def adapter(self, engine, kind=None, **kwargs):

        ''' Acquire a write-capable driver for ``engine``, constructing
            if needed. Available options for ``engine`` are enumerated
            at :py:attr:`EventEngine.Datastore`.

            :param engine: Engine :py:class:`model.adapter.ModelAdapter`
            to acquire an adapter to.

            :param kind: Model ``kind`` name to provision an adapter
            instance for. ``None`` indicates that a general adapter
            with default settings should be returned. Defaults to
            ``None``.

            :param **kwargs: Keyword arguments to pass to the newly-
            acquired adapter.

            :returns: Newly-prepared/constructed :py:class:`RedisAdapter`,
            :py:class:`MemcacheAdapter`, or :py:class:`InMemoryAdapter`,
            depending on the value passed in at ``engine``. '''

        if kind: return engine(**kwargs).channel(kind)
        return engine(**kwargs)

    def pipeline(self, engine=Datastore.redis, kind=None):

        ''' Begin execution buffering in the context of an existing
            or newly-created ``Redis`` pipeline.

            :param engine: Datastore engine to actquire a pipeline
            for. Choices available at the encapsulated local enum
            at :py:attr:`EventEngine.Datastore`. Defaults to
            :py:class:`EventEngine.Datastore.redis`.

            :param kind: String ``kind`` name to pass to adapter
            methods like :py:meth:`adapter.channel`. Defaults to
            ``None``.

            :returns: :py:class:`redis.client.StrictPipeline`, in
            the case that ``engine`` is ``Datastore.redis`` and
            pipelining is supported. Otherwise returns ``None``. '''

        return self.adapter(engine, kind).channel(kind).pipeline()

    ## === Public Methods === ##
    def persist(self, entity, pipeline=None):

        ''' Persist an event using underlying data storage
            mechanisms. Tries as hard as it can to use
            pipeline-enabled Redis, but falls back to
            :py:class:`InMemoryAdapter` in the case that it
            is not supported.

            :param entity: Entity in question that needs to
            be persisted in storage.

            :param pipeline: Existing pipeline-like object
            to use in place of a newly constructed one.
            Defaults to ``None``.

            :returns: Persisted :py:class:`model.Key` for
            the newly-written entity, or ``pipeline`` if
            a valid pipeline was passed in. '''

        # if pipelining is enabled and supported, start a new one...
        if pipeline and _REDIS and (entity.key.id is not None):

            batch = pipeline
            if not isinstance(pipeline, (client.StrictPipeline, client.Pipeline)):
                # and put the entity, using the pipeline... then return it
                batch = self.pipeline()
            return entity.key, entity.put(pipeline=batch)

        # otherwise, put the entity normally and return the written key
        return entity.put()

    def publish(self, channels, value, execute=True, pipeline=None):

        ''' Low-level method to publish a message to
            ``Redis`` pub/sub.

            :param channels: Either a ``str`` name for a channel
            to publish this value on, or an iterable of ``str``
            channel names.

            :param value: ``protorpc.Message`` class, ``dict``,
            or raw string to publish.

            :keyword execute: Boolean flag indicating whether
            :py:meth:`publish` should flush the internal
            pipeline after building, or return it for further
            operation. Defaults to ``True``.

            :keyword pipeline: Replacement, existing pipeline
            object to use instead of a new one. Defaults to
            ``None``.

            :returns: The result of the low-level publish
            operation. '''

        from protorpc import messages
        from apptools.rpc import mappers

        # first, resolve value
        if not isinstance(value, (dict, messages.Message, basestring)):
            raise ValueError('Can only pubsub strings, `protorpc.Message` and `dict`.')

        elif isinstance(value, (dict, messages.Message)):
            encoded = mappers.JSONRPC._MessageJSONEncoder().encode(value)
        else:
            encoded = value  # must be a string

        if _REDIS:
            if isinstance(channels, (tuple, list)):

                # for multiple channels, start a pipeline
                pipe = pipeline if pipeline is not None else self.pipeline(self.Datastore.redis)
                for channel in channels:
                    pipe.publish(channel, encoded)

                if execute:
                    # execute pipeline
                    return pipe.execute()
                return pipe

            else:
                channel = channels
                return self.adapter(self.Datastore.redis, 'Realtime').publish(channel, encoded)
        else:
            message = 'PubSub disabled, but would publish to channels "%s" with content "%s".' % (channels, value)
            self.logging.info(message)
            return

    def subscribe(self, channel, pattern=False, _start=False):

        ''' Low-level method to subscribe to one or
            multiple ``Redis`` pub/sub streams.

            :param channel: Target channel to subscribe to,
            or pattern of channels to subscribe to.

            :param pattern: Flag (``bool``) indicating whether the
            ``channel`` value is a pattern or literal channel name.
            Defaults to ``False``.

            :param _start: Schedule the ``Greenlet`` for
            immediate execution before returning. Defaults to
            ``False``.

            :returns: An optionally-started ``Greenlet``,
            which block-listens for new subscribed
            messages. '''

        raise NotImplementedError('Method `subscribe` is not yet supported.')

    def increment(self, bucket, delta=1, pipeline=None, force_toplevel=False):

        ''' Increment the value of a counter bucket (located
            at ``bucket``) by the value at ``delta``.

            :param bucket: Name (``str``) of the counter
            bucket key to increment.

            :param delta: Value (``int``, ``float`` or ``long``)
            to adjust the running total of the target counter by.
            For example, a delta of ``1`` (the default value) will
            add ``1`` to the value at ``bucket``, creating it (and
            conveniently defaulting it to ``0``) the proper bucket
            if it doesn't exist.

            :param pipeline: Existing pipeline buffer to use for
            writes that take place in this method. Defaults to
            ``None``.

            :param force_toplevel: Flag (``bool``) indicating that
            we wish to force all storage operations to occur in the
            top-level datastore namespace (disables hash bucketing).

            :raises TypeError: In the case of an invalid type
            for ``bucket``, which only accepts ``basestring``.

            :raises TypeError: In the case of an invalid type
            for ``delta``, which only accepts ``float``, ``int``
            and ``long``.

            :raises ValueError: In the case that ``delta`` is
            less than 1.

            :returns: Result of the low-level datastore increment
            operation, or ``pipeline`` if a valid pipeline was
            presented. '''

        from protocol.special import Separators

        # check delta type
        if not isinstance(delta, (float, int)):
            raise TypeError('`delta` value for counter increment operation on '
                            'bucket "%s" must be an integer or float, got %s.' % (bucket, type(delta)))

        if delta < 0:
            raise ValueError('`delta` value for counter increment must be '
                             'greater than 1. Got: "%s".' % delta)

        # check bucket type
        if not isinstance(bucket, basestring):
            raise TypeError('`bucket` key for counter increment operation must '
                            'be a string. Received: "%s" of type "%s".' % (bucket, type(bucket)))

        if _REDIS:

            # resolve whether we're going to be hashing our value
            use_hash = True
            if force_toplevel or (self.redis.EngineConfig.mode is redis.RedisMode.toplevel_blob):
                use_hash = False
            else:
                bucket_split = bucket.split(Separators.HASH_CHUNK)
                key_prefix = Separators.HASH_CHUNK.join(bucket_split[:2])
                key_postfix = Separators.HASH_CHUNK.join(bucket_split[2:])

            # resolve write method
            if isinstance(delta, int):

                if use_hash:
                    handler, opargs = self.redis.Operations.HASH_INCREMENT, (key_prefix, key_postfix, delta)
                else:
                    handler, opargs = self.redis.Operations.INCREMENT, (bucket, delta)

            elif isinstance(delta, float):

                if use_hash:
                    handler, opargs = self.redis.Operations.HASH_INCREMENT_FLOAT, (key_prefix, key_postfix, delta)

                else:
                    handler, opargs = self.redis.Operations.INCREMENT_BY_FLOAT, (bucket, delta)

            # execute operation, optionally against a pipeline
            return self.Datastore.redis.execute(handler, None, *opargs, target=pipeline)

    def index_add(self, bucket, value, pipeline=None):

        ''' Add the value at ``value`` to the container index
            specified at ``bucket``.

            :param bucket: Bucket identifier (``str``) that specifies
            the index we wish to write to.

            :param value: Value to add to the index. How the value
            is written and what structure is used depends on the
            adapter selected for the write.

            :param pipeline: Existing low-level pipeline to execute
            the write(s) against, in place of the mainline adapter.
            Defaults to ``None``.

            :raises NotImplementedError: Always, as this method is
            currently stubbed.

            :returns: Result of the low-level write operation, or
            ``pipeline`` if a valid pipeline was presented. '''

        raise NotImplementedError('`EventTracker` does not yet support compound key indexes.')
