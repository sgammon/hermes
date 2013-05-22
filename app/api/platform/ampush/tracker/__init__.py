# -*- coding: utf-8 -*-

"""
This package contains platform-specific code for `EventTracker`, and
is the primary location for app-wide business logic.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# Base Imports
import webapp2

# Platform Parent
from api.platform import Platform

# Model Adapters
from apptools.model.adapter import redis
from apptools.model.adapter import inmemory

# Platform Bridges
from api.platform.ampush.tracker import stream


## Tracker - version one of the `EventTracker` platform
class Tracker(Platform):

    ''' Version 1 of `EventTracker` platform. '''

    # Class Constants
    _config_path = 'platform.ampush.tracker.Tracker'

    ## DatastoreEngine - static, encapsulated adapter import.
    class DatastoreEngine(object):

        ''' Encapsulated attachment of symbols to
            :py:mod:`model.adapter.redis` and
            :py:mod:`model.adapter.inmemory`. '''

        redis = redis.RedisAdapter
        memory = inmemory.InMemoryAdapter

    def initialize(self):

        ''' Initialize the ``Tracker`` platform, and attach
            any encapsulated classes.

            :returns: The currently-active :py:class:`Tracker`, for chainability. '''

        # Platform Bridges
        self.stream = stream.EventStream(self)

        return self

    @classmethod
    def check_environment(cls, environ, config):

        ''' Check if the current environment supports Tantric.

            :param environ: Current non-runtime environment ``dict``.
            :param config: System-wide configuration ``dict``.
            :returns: Boolean indicating whether this ``Platform``
                      should be loaded. '''

        return True

    @webapp2.cached_property
    def shortcut_exports(self):

        ''' Return shortcuts.
            :returns: List of ``(<name>, <obj>)`` pairs to create
                      shortcuts on target base classes for. '''

        # Shortcut exports
        return [
            ('tracker', self)
        ]

    @webapp2.cached_property
    def template_context(self):

        ''' Inject Tracker-specific template context.
            :returns: Callable function :py:func:`inject_tracker`,
                      which can be deferred until template
                      construction time, and returns context
                      mutations for this particular ``Platform``. '''

        def inject_tracker(handler, context):

            ''' Protocol/platform stuff.

                :param handler: The currently-active descendent of
                                :py:class:`webapp2.RequestHandler`.

                :param context: Template context ``dict`` to be
                                optionally mutated and returned.

                :returns: Materialized context ``dict``. '''

            return context

        return inject_tracker

    ## == Tracker Internals == ##
    def resolve(self, raw_event):

        ''' Resolves a ``model.Tracker`` for a given
            ``model.RawEvent``.

            :param raw_event: Object :py:class:`model.RawEvent` to
                              resolve a :py:class:`model.Tracker` for.
            :returns: An inflated ``model.Tracker`` object. '''

        pass

    ## == Dispatch Hooks == ##
    def pre_dispatch(self, handler):

        ''' Invoked right before handler dispatch.

            :param handler: The currently-active descendent of
                            :py:class:`webapp2.RequestHandler`.

            :returns: The very same ``handler``, post-mutation. '''

        return handler

    def post_dispatch(self, handler, response):

        ''' Invoked right after handler dispatch.

            :param handler: The currently-active descendent of
                            :py:class:`webapp2.RequestHandler`.

            :returns: Nothing, the return value from this method is
                      **discarded**, since the response has already
                      been relayed to the requesting party. '''

        return
