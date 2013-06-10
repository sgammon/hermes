# -*- coding: utf-8 -*-

'''

Aggregation Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# stdlib
import time
import config
import hashlib
import datetime

# apptools
from apptools import rpc

# Protocol
from protocol import meta
from protocol import special
from protocol import timedelta


## Aggregation
# Specification class for an aggregated property.
class Aggregation(meta.ProtocolBinding, rpc.ConfiguredClass):

    ''' Specifies an aggregation operation to be performed on
        one or more properties upon an event matching a profile
        that provides this ``Aggregation``. '''

    _config_path = 'protocol.aggregation.Aggregation'

    ## == State == ##
    name = None  # name of this aggregation
    prop = None  # owning property of this aggregation
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

    ## == Timewindow Builders == ##
    def _day_timewindow(self, stamp):

        ''' Build a timewindow for a day. '''

        # generates timestamp with day-level granularity
        return str(int(time.mktime(stamp.date().timetuple())) / 1e2)

    def _week_timewindow(self, window, stamp):

        ''' Build a timewindow for a week. '''

        # like: ``<year>:<week #>``
        calendar = stamp.date().isocalendar()
        if window != timedelta.TimeWindow.ONE_WEEK:
            return self._WINDOW_SEPARATOR.join(map(unicode, calendar[:-1] + ((window - 1) + calendar[1])))
        return self._WINDOW_SEPARATOR.join(map(unicode, calendar[:-1]))

    def _month_timewindow(self, window, stamp):

        ''' Build a timewindow for a month. '''

        # like: ``<year>:<month>``
        if window != timedelta.TimeWindow.ONE_MONTH:
            return self._WINDOW_SEPARATOR.join(map(unicode, (stamp.year, stamp.month, (stamp.month + (window - 7)))))
        return self._WINDOW_SEPARATOR.join(map(unicode, (stamp.year, stamp.month)))

    def _year_timewindow(self, window, stamp):

        ''' Build a timewindow for a year. '''

        return unicode(stamp.year)

    def _global_timewindow(self, window, stamp):

        ''' Build a timewindow for ``FOREVER``. '''

        return self._GLOBAL_WINDOW

    _window_builders = {
        timedelta.TimeWindow.ONE_DAY: _day_timewindow,
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
        result = self._window_builders.get(interval, self._global_timewindow)(interval, created)

        # log the result if debug is enabled
        if config.debug and not config.production:
            context = (interval, created, result)
            self.logging.info('Built timewindow for interval `%s` and timestamp `%s`: "%s".' % context)
        return result

    def _build_perms(self, policy, data):

        ''' Build permutations for this ``Aggregation``. '''

        pass

    def _build_spec(self, policy, data):

        ''' Build bucket specifications for this ``Aggregation``. '''

        import pdb; pdb.set_trace()

    ## == Public Methods == ##
    def set_owner(self, property):

        ''' Set the encapsulating property that holds this ``Aggregation``.
            Done at construction time by the :py:attr:`cls.Interpreter`. '''

        self.prop = property
        return self

    def build(self, policy, data):

        ''' Build this ``Aggregation``, and all attached
            permutations. '''

        return self

    def __call__(self, policy, data):

        ''' Proxy for ``__call__`` to a nested generator
            that will yield all ``Attributions`` for this
            spec. '''

        pass
