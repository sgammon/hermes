# -*- coding: utf-8 -*-

'''

Aggregation Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# stdlib
import time
import config
import base64
import hashlib
import datetime

# Protocol
from protocol import meta
from protocol import special
from protocol import timedelta

# apptools util
from apptools.util import debug
from apptools.util import decorators


## Aggregation
# Specification class for an aggregated property.
class Aggregation(meta.ProtocolBinding):

    ''' Specifies an aggregation operation to be performed on
        one or more properties upon an event matching a profile
        that provides this ``Aggregation``. '''

    _config_path = 'protocol.aggregation.Aggregation'

    ## == State == ##
    name = None  # name of this aggregation
    prop = None  # target properties of this aggregation
    interval = None  # intervals we wish to aggregate for
    permutations = None  # permutations of this aggregation

    ## == Internals == ##
    _BUCKET_PREFIX = special.Prefixes.AGGREGATION  # prefix for bucket name (usually `__aggregation__`)
    _GLOBAL_WINDOW = timedelta._GLOBAL_WINDOW_POSTFIX  # special postfix window indicating a global aggregation interval
    _NAME_SEPARATOR = special.Separators.HASH_KEY_NAME  # char for bucket name items (ie. `my-index` would be `-`)
    _CHUNK_SEPARATOR = special.Separators.HASH_CHUNK  # char for chunks of key=>value pairs (ie. `__index__::blab`)
    _WINDOW_SEPARATOR = special.Separators.HASH_KEY_VALUE  # char for bucket value items (ie. `2013:01` would be `:`)

    def __init__(self, name, **config):

        ''' Initialize this ``Aggregation``. '''

        # set name + interval, default interval is ``FOREVER`` (global count), set empty tuple of perms
        self.name, self.interval = name, config.get('interval', timedelta.TimeWindow.FOREVER)
        self.permutations = config.get('permutations', tuple())

    def _hashhex(self, value):

        ''' Hash the target value according to the current
            settings for bucket key hashing. '''

        if self.config.get('hasher', {}).get('enabled', False) is True:
            return self.config.get('hasher', {}).get('algorithm', hashlib.sha1)(value).hexdigest()
        return value

    @decorators.memoize
    @decorators.classproperty
    def config(cls):

        ''' Local config pipe. '''

        return config.config.get(cls._config_path, {'debug': True})

    @decorators.memoize
    @decorators.classproperty
    def logging(cls):

        ''' Local logging pipe. '''

        # split config path
        _split = cls._config_path.split('.')

        # factory logger
        return debug.AppToolsLogger(**{
            'path': '.'.join(_split[0:-1]),
            'name': _split[-1]
        })._setcondition(cls.config.get('debug', True))

    ## == Timewindow Builders == ##
    def _hour_timewindow(self, window, stamp):

        ''' Build a timewindow for an hour. '''

        return str(int(time.mktime(datetime.datetime(**{
            'year': stamp.year,
            'month': stamp.month,
            'day': stamp.day,
            'hour': stamp.hour
        }).timetuple()) / 1e2))

    def _day_timewindow(self, window, stamp):

        ''' Build a timewindow for a day. '''

        # generates timestamp with day-level granularity
        return str(int(time.mktime(stamp.date().timetuple()) / 1e3))

    def _week_timewindow(self, window, stamp):

        ''' Build a timewindow for a week. '''

        # like: ``<year>:<week #>``
        calendar = stamp.date().isocalendar()
        if window != timedelta.TimeWindow.ONE_WEEK:
            return self._WINDOW_SEPARATOR.join(map(unicode, list(calendar[:-1])))
        return self._WINDOW_SEPARATOR.join(map(unicode, calendar[:-1]))

    def _month_timewindow(self, window, stamp):

        ''' Build a timewindow for a month. '''

        # like: ``<year>:<month>``
        if window != timedelta.TimeWindow.ONE_MONTH:
            return self._WINDOW_SEPARATOR.join(map(unicode, (stamp.year, stamp.month)))
        return self._WINDOW_SEPARATOR.join(map(unicode, (stamp.year, stamp.month)))

    def _year_timewindow(self, window, stamp):

        ''' Build a timewindow for a year. '''

        return unicode(stamp.year)

    def _global_timewindow(self, window, stamp):

        ''' Build a timewindow for ``FOREVER``. '''

        return self._GLOBAL_WINDOW

    _window_builders = {
        timedelta.TimeWindow.ONE_DAY: _day_timewindow,
        timedelta.TimeWindow.ONE_HOUR: _hour_timewindow,
        timedelta.TimeWindow.TWO_HOURS: _hour_timewindow,
        timedelta.TimeWindow.THREE_HOURS: _hour_timewindow,
        timedelta.TimeWindow.FOUR_HOURS: _hour_timewindow,
        timedelta.TimeWindow.FIVE_MONTHS: _hour_timewindow,
        timedelta.TimeWindow.SIX_MONTHS: _hour_timewindow,
        timedelta.TimeWindow.ONE_WEEK: _week_timewindow,
        timedelta.TimeWindow.TWO_WEEKS: _week_timewindow,
        timedelta.TimeWindow.THREE_WEEKS: _week_timewindow,
        timedelta.TimeWindow.FOUR_WEEKS: _week_timewindow,
        timedelta.TimeWindow.FIVE_WEEKS: _week_timewindow,
        timedelta.TimeWindow.SIX_WEEKS: _week_timewindow,
        timedelta.TimeWindow.MONTH: _month_timewindow,
        timedelta.TimeWindow.TWO_MONTHS: _month_timewindow,
        timedelta.TimeWindow.THREE_MONTHS: _month_timewindow,
        timedelta.TimeWindow.FOUR_MONTHS: _month_timewindow,
        timedelta.TimeWindow.FIVE_MONTHS: _month_timewindow,
        timedelta.TimeWindow.SIX_MONTHS: _month_timewindow,
        timedelta.TimeWindow.YEAR: _year_timewindow,
        timedelta.TimeWindow.FOREVER: _global_timewindow
    }

    ## == Component Builders == ##
    def _build_name(self, permutation):

        ''' Build a name for a permutation of this ``Aggregation``. '''

        return self._NAME_SEPARATOR.join((self.name, permutation))

    def _build_window(self, interval, created):

        ''' Build a timewindow and delta value for a given
            ``interval`` and ``created`` timestamp. '''

        # calculate timewindow string
        result = self._window_builders.get(interval, self._global_timewindow)(self, interval, created)
        return result

    def _build_spec(self, policy, event):

        ''' Build bucket specifications for this ``Aggregation``. '''

        final = []
        hashspec = [self._BUCKET_PREFIX, self.name]

        # add prop windows
        for i, prop in enumerate(self.prop):

            if prop.basetype is float or prop.literal is True:

                # direct delta value
                delta = event.params.get(prop.name)

            else:

                # resolve parameter and value
                delta, value = 1, event.params.get(prop.name)

                if value is None:
                    self.logging.warning('Failed to calculate aggregation '
                                         '%s because property "%s" was found '
                                         'to have a null value.' % (self, prop))
                    continue

                b64_value = base64.b64encode(value)
                self.logging.debug('Encoding value "%s" to b64 "%s".' % (value, b64_value))
                hashspec.append(b64_value)

            # calculate intervals only on last iteration or if we have 1 origin
            if len(self.prop) < 2 or (i is len(self.prop) - 1):
                for interval in self.interval:
                    final.append(self._CHUNK_SEPARATOR.join(hashspec + [str(interval), self._build_window(interval, event.created)]))

        return delta, tuple(final)

    def _build_perms(self, policy, event):

        ''' Build permutations for this ``Aggregation``. '''

        for perm, props in self.permutations:

            # build owner properties
            owners = self.prop[:]
            if not isinstance(props, (list, set, frozenset, tuple)):
                props = (props,)

            for prop in props:
                owners.append(policy.resolve_parameter(prop))

            # build sub-aggregation
            permutation = Aggregation(self._build_name(perm), interval=self.interval).set_owner(owners)

            # recursively yield specs
            for aggregation, spec in permutation.build(policy, event):
                yield aggregation, spec

    ## == Public Methods == ##
    def set_owner(self, property):

        ''' Set the encapsulating property that holds this ``Aggregation``.
            Done at construction time by the :py:attr:`cls.Interpreter`. '''

        # iterable-ify if it's not iterable
        if not isinstance(property, list):
            property = [property]

        self.prop = property
        return self

    def build(self, policy, event):

        ''' Build this ``Aggregation``, and all attached
            permutations. '''

        # build local aggregation
        yield self._build_spec(policy, event)

        for perm, spec in self._build_perms(policy, event):
            yield perm, spec

    def __call__(self, policy, event):

        ''' Proxy for ``__call__`` to a nested generator
            that will yield all ``Attributions`` for this
            spec. '''

        # set owner and build
        for aggregation, spec in self.build(policy, event):
            yield spec
