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

# Model Adapters
from apptools.model.adapter import redis
from apptools.model.adapter import memcache
from apptools.model.adapter import inmemory

try:
    import redis; _REDIS = True
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
        memcache = memcache.MemcacheAdapter

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

        pass

    ## === Bindings === ##
    def adapter(self, engine, kind=None, **kwargs):

        ''' Acquire a write-capable driver for ``engine``, constructing
            if needed. Available options for ``engine`` are enumerated
            at :py:attr:`EventEngine.Datastore`.

            :param engine: Engine :py:class:`model.adapter.ModelAdapter`
                           to acquire an adapter to.

            :param **kwargs: Keyword arguments to pass to the newly-
                             acquired adapter.

            :returns: Newly-prepared/constructed :py:class:`RedisAdapter`,
                      :py:class:`MemcacheAdapter`, or :py:class:`InMemoryAdapter`,
                      depending on the value passed in at ``engine``. '''

        e = engine(**kwargs)
        if kind:
            return e.channel(kind)
        return e

    ## === Public Methods === ##
    def pipeline(self, engine=Datastore.redis, kind='Realtime'):

        ''' Begin execution buffering in the context of an existing
            or newly-created ``Redis`` pipeline.

            :param kind: String ``kind`` name to pass to adapter
                         methods like :py:meth:`adapter.channel()`.

            :returns: :py:class:`redis.client.StrictPipeline`. '''

        return self.adapter(engine, kind).pipeline()

    def persist(self, entity, pipeline=False):

        ''' Persist an event. '''

        # save entity
        return entity.put()

    def publish(self, channels, value):

        ''' Low-level method to publish a message to
            ``Redis`` pub/sub.

            :param channels: Either a ``str`` name for a channel
            to publish this value on, or an iterable of ``str``
            channel names.

            :param value: ``protorpc.Message`` class, ``dict``,
            or raw string to publish.

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
                with self.pipeline(self.Datastore.redis) as pipeline:
                    for channel in channels:
                        pipeline.publish(channel, encoded)

                    # execute pipeline
                    result = pipeline.execute()
                return result

            else:
                channel = channels
                return self.adapter(self.Datastore.redis, 'Realtime').publish(channel, encoded)
        else:
            self.logging.info('PubSub disabled, but would publish to channels "%s" with content "%s".' % (channels, value))
            return

    def subscribe(self, channel, pattern=False):

        ''' Low-level method to subscribe to one or
            multiple ``Redis`` pub/sub streams.

            :keyword _start: Schedule the ``Greenlet`` for
            immediate execution before returning.

            :returns: An optionally-started ``Greenlet``,
            which block-listens for new subscribed
            messages. '''

        pass
