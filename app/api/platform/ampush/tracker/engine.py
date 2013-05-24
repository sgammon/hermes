# -*- coding: utf-8 -*-

'''
The :py:class:`EventEngine` class handles calls to
underlying storage mechanisms.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Platform Parent
from api.platform import PlatformBridge

# Model Adapters
from apptools.model.adapter import redis
from apptools.model.adapter import memcache
from apptools.model.adapter import inmemory

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
    @property
    def adapter(self, engine, *args, **kwargs):

        ''' Acquire a write-capable driver for ``engine``, constructing
            if needed. Available options for ``engine`` are enumerated
            at :py:attr:`EventEngine.Datastore`.

            :param engine: Engine :py:class:`model.adapter.ModelAdapter`
                           to acquire an adapter to.

            :param *args: Positional arguments to pass to the newly-
                          acquired adapter.

            :param **kwargs: Keyword arguments to pass to the newly-
                             acquired adapter.

            :returns: Newly-prepared/constructed :py:class:`RedisAdapter`,
                      :py:class:`MemcacheAdapter`, or :py:class:`InMemoryAdapter`,
                      depending on the value passed in at ``engine``. '''

        pass

    ## === Public Methods === ##
    def pipeline(self):

        ''' Begin execution buffering in the context of an existing
            or newly-created ``Redis`` pipeline.

            :returns: :py:class:`redis.client.StrictPipeline`. '''

        pass

    def publish(self, channel, value):

        ''' Low-level method to publish a message to
            ``Redis`` pub/sub.

            :param channel: Either a ``str`` name for a channel
                            to publish this value on, or an
                            iterable of ``str`` channel names.

            :param value: Dictionary to be encoded and published
                          via ``pubsub``.

            :returns: The result of the low-level publish
                      operation. '''

        pass

    def subscribe(self, channel, pattern=False):

        ''' Low-level method to subscribe to one or
            multiple ``Redis`` pub/sub streams.

            :keyword _start: Schedule the ``Greenlet`` for
                             immediate execution before
                             returning.

            :returns: An optionally-started ``Greenlet``,
                      which block-listens for new subscribed
                      messages. '''

        pass
