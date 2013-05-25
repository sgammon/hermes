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

# Platform Bridges
from api.platform.tracker import event
from api.platform.tracker import stream
from api.platform.tracker import engine
from api.platform.tracker import policy


## Tracker - version one of the `EventTracker` platform
class Tracker(Platform):

    ''' Version 1 of `EventTracker` platform. '''

    # Constants
    vesion = (0, 1)
    _config_path = 'platform.tracker.Tracker'

    def initialize(self):

        ''' Initialize the ``Tracker`` platform, and attach
            any encapsulated classes.

            :returns: The currently-active :py:class:`Tracker`, for chainability. '''

        # Platform Bridges
        self.event = event.EventBuilder(self)  # event inflator/intake
        self.stream = stream.EventStream(self)  # eventstream pubsub tools
        self.engine = engine.EventEngine(self)  # low-level IO engine
        self.policy = policy.PolicyEngine(self)  # policy enforcement engine

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

    def provision(self, *args, **kwargs):

        ''' Entrypoint for provisioning/creating a new
            :py:class:`api.models.tracker.endpoint.Tracker`.

            :param *args: Positional arguments to pass to
                          the :py:class:`endpoint.Tracker`
                          construction routine.

            :param **kwargs: Keyword arguments to pass to
                             the :py:class:`endpoint.Tracker`
                             construction routine.

            :returns: The newly-created :py:class:`endpoint.Tracker`. '''

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
