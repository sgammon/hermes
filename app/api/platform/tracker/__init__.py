# -*- coding: utf-8 -*-

"""
This package contains platform-specific code for `EventTracker`, and
is the primary location for app-wide business logic.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# stdlib
import datetime

# 3rd party
from protorpc import messages

# Protocol Suite
from protocol import timedelta

# Platform Parent
from api.platform import Platform

# apptools
from apptools import model
from apptools.util import decorators

# Tracker Models
from api.models.tracker import endpoint

# Platform Bridges
from api.platform.tracker import event
from api.platform.tracker import stream
from api.platform.tracker import engine
from api.platform.tracker import policy


## Tracker - version one of the `EventTracker` platform
class Tracker(Platform):

    ''' Version 0.1 of `EventTracker` platform. '''

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

    @decorators.memoize
    def shortcut_exports(self):

        ''' Return shortcuts.
            :returns: List of ``(<name>, <obj>)`` pairs to create
                      shortcuts on target base classes for. '''

        # Shortcut exports
        return [
            ('tracker', self)
        ]

    @decorators.memoize
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

    ## == Utilities == ##
    def resolve_timewindow(self, window, delta, scope=None):

        ''' Resolves a timewindow. '''

        if not isinstance(window, int):
            window = int(window)

        # decode window: special cases first

        # day-level window
        if window is timedelta.TimeWindow.ONE_DAY:
            _day_ts = int(int(delta) * 1e2)
            delta_begin = datetime.datetime.fromtimestamp(_day_ts)
            delta_end = delta_begin + datetime.timedelta(days=1)

            if scope:
                identifier = (scope.DAY, 1)

        # year-level window
        elif window is timedelta.TimeWindow.YEAR:
            _year_ts = int(delta)
            delta_begin = datetime.datetime(year=_year_ts, month=1, day=1)
            delta_end = delta_begin + datetime.timedelta(days=365)

            if scope:
                identifier = (scope.YEAR, 1)

        # global window
        elif window is timedelta.TimeWindow.FOREVER:
            delta_begin, delta_end = None, None

            if scope:
                identifier = (scope.FOREVER, 1)

        # hour-level window
        elif timedelta.TimeWindow.ONE_DAY < window < timedelta.TimeWindow.ONE_WEEK:

            _hour_ts = (window - (timedelta.TimeWindow.ONE_HOUR - 1))
            delta_begin = datetime.datetime.fromtimestamp(int(int(delta) * 1e2))
            delta_end = delta_begin + datetime.timedelta(hours=_hour_ts)

            if scope:
                identifier = (scope.HOUR, _hour_ts)

        # week-level window
        elif timedelta.TimeWindow.SIX_HOURS < window < timedelta.TimeWindow.MONTH:

            _week_ts = window - (timedelta.TimeWindow.ONE_WEEK - 1)
            split = delta.split(self.engine._chunk_separator)
            year, week = int(split[0]), int(split[1])

            delta_begin = datetime.datetime.strptime("%04d-%02d-1" % (year, week), "%Y-%W-%w")
            delta_end = delta_begin + (datetime.timedelta(days=(7 * _week_ts)))

            if scope:
                identifier = (scope.WEEK, _week_ts)

        # month-level window
        elif timedelta.TimeWindow.SIX_WEEKS < window < timedelta.TimeWindow.YEAR:

            split = delta.split(self.engine._chunk_separator)
            year, month = int(split[0]), int(split[1])

            delta_begin = datetime.datetime(year=year, month=month, day=1)

            month_delta = (window - (timedelta.TimeWindow.MONTH - 1))
            if month + month_delta > 12:
                delta_end = datetime.datetime(year=(year + 1), month=((month + month_delta) - 12))
            else:
                delta_end = datetime.datetime(year=year, month=(month + month_delta))

            if scope:
                identifier = (scope.MONTH, month_delta)

        else:
            raise ValueError('Invalid window `%s` provided to `resolve_timewindow`.' % window)

        if not scope:
            identifier = window

        return identifier, (delta_begin, delta_end)

    ## == Tracker Internals == ##
    def resolve(self, raw, base_policy=None, legacy=False):

        ''' Resolves a ``model.Tracker`` for a given
            ``webapp2.Request``.

            :param raw: Raw event object to resolve a tracker
            from (:py:class:`api.models.tracker.raw.Event`).

            :keyword base_policy: Base policy suite to consider.

            :returns: Tuple with inflated ``model.Tracker`` object
            and passed-in base policy, to be used down the
            policy processing flow at ``tracker.policy.interpret``. '''

        tracker = None

        if not legacy:  # only look up/use trackers when not in legacy mode

            raise Exception('Non-legacy tracking not yet supported.')

        return raw, tracker

    def provision(self, owner, specs=None, spec=None):

        ''' Entrypoint for provisioning/creating new
            :py:class:`api.models.tracker.endpoint.Tracker` objects.

            :param owner: Parent owner of the :py:class:`endpoint.Tracker`
            to be constructed. Must be of type ``basestring``. Raises
            :py:exc:`ValueError` if another type of value is provided.
            How it is used depends on the underlying driver.

            :param specs: Iterable of ``object`` or ``dict``-like items
            that should be expanded, ``**kwargs``-style, into trackers.
            Generates/allocates one :py:class:`endpoint.Tracker` per spec.

            :param spec: Syntactic sugar for passing in a single spec. Using
            this parameter is guaranteed to return only a single
            :py:class:`endpoint.Tracker` - not an iterable.

            :raises TypeError: If ``owner`` is not of type
            ``int`` or ``long``.

            :raises ValueError: If ``specs`` or ``spec`` receives an invalid
            :py:class:`endpoint.Tracker` specification. Allowed types are
            ``dict`` or ``message.Message``.

            :returns: The newly-created :py:class:`endpoint.Tracker` objects,
            in a ``list``. If one :py:class:`endpoint.Tracker` is requested, it is
            returned directly - not in a one-item iterable. '''

        if not isinstance(owner, basestring):
            raise TypeError('Argument `owner` to platform method `provision` must be of type `int` or `long`. '
                            'Got: "%s".' % str(owner))

        # provision tracker IDs
        datastore = self.engine.Datastore.redis if self.engine._REDIS_ENABLED else self.engine.Datastore.inmemory

        # make sure we have a clean iterable
        if spec:
            specs = [spec]
        elif isinstance(specs, (dict, messages.Message)):
            specs = [specs]

        # synchronously provision IDs
        ids = self.engine.adapter(datastore).allocate_ids(*(
            endpoint.Tracker().key.__class__,
            endpoint.Tracker.kind(),
            len(specs)
        ))

        if not isinstance(ids, (tuple, list)):
            ids = [ids]

        _trackers, pipeline = [], self.engine.pipeline() if len(specs) > 1 else None
        for spec, id in zip(specs, ids):

            ## expand dictionary spec
            if isinstance(spec, dict):
                spec['key'], spec['owner'] = model.Key(endpoint.Tracker, id), id
                t = endpoint.tracker(**spec)

            ## expand message spec
            elif isinstance(spec, messages.Message):
                t = endpoint.Tracker(**{
                    'key': model.Key(endpoint.Tracker, id),
                    'owner': owner,
                    'profile': spec.profile
                })

            else:
                raise ValueError('Argument `specs` or `spec` got an invalid spec for '
                                 'provisioning a Tracker. Expected `dict` or `message.Message`. Got "%s".' % str(spec))

            t.put(pipeline=pipeline)
            _trackers.append(t)

        if pipeline:  # execute pipeline and return
            pipeline.execute()

        if len(specs) is 1:  # return directly if only one was requested
            return _trackers[0]
        return _trackers

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
