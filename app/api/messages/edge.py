# -*- coding: utf-8 -*-

'''
Holds structured :py:class:`protorpc.Message` classes for expressing
:py:class:`TrackedEvent` edges (such as :py:class:`protocol.Attribution` and
:py:class:`protocol.Aggregation` objects).

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# apptools rpc
from apptools import rpc


## Timewindow
# Expresses a window of time for which aggregated or attributed events have occurred.
class Timewindow(rpc.messages.Message):

    ''' Expresses a timewindow for which aggregated
        or attributed values are available. '''

    ## WindowScope - expresses the type of window in use.
    class WindowScope(rpc.messages.Enum):

        ''' Enumerates options for types/sizes
            available for use as a :py:class:`Timewindow`. '''

        HOUR = 0x1
        DAY = 0x2
        WEEK = 0x4
        MONTH = 0x5
        YEAR = 0x6
        FOREVER = 0x0

    scope = rpc.messages.EnumField(WindowScope, 1)
    delta = rpc.messages.IntegerField(2)
    start = rpc.messages.IntegerField(3)
    end = rpc.messages.IntegerField(4)


## Aggregation
# Expresses an aggregation generated for a property (or combination of properties) across many events.
class Aggregation(rpc.messages.Message):

    ''' Expresses a single aggregated value, in the
        context of a :py:class:`Timewindow`. '''

    value = rpc.messages.VariantField(1)
    window = rpc.messages.MessageField(Timewindow, 2)


## PropertyValue
# Holds a single property=>value pair.
class PropertyValue(rpc.messages.Message):

    ''' Expresses a single property=>value mapping
        pair. '''

    property = rpc.messages.StringField(1, required=True)
    value = rpc.messages.VariantField(2, required=True)


## AggregationGroup
# Expresses a group of timewindow-scoped values that share an aggregation dimension.
class AggregationGroup(rpc.messages.Message):

    ''' Expresses a set of :py:class:`Timewindow`-scoped,
        aggregated values that share the same aggregation
        dimension. '''

    data = rpc.messages.MessageField(Aggregation, 1, repeated=True)
    spec = rpc.messages.MessageField(PropertyValue, 2, repeated=True)


## Attribution
# Expresses an attribution generated for a property (or combination of properties) across many events.
class Attribution(rpc.messages.Message):

    ''' Expresses an individual :py:class:`protocol.Attribution`,
        or attributed group of keys/values for a given
        :py:class:`event.TrackedEvent`. '''

    pass  # STUBBED


## AttributionGroup
# Expresses a set of individual, time-scoped attributions for a given :py:class:`TrackedEvent`.
class AttributionGroup(rpc.messages.Message):

    ''' Expresses a group of :py:class:`Attribution` records,
        scoped by a :py:class:`Timewindow`, that share the
        same :py:class:`TrackedEvent`. '''

    pass  # STUBBED
