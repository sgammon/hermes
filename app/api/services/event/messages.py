# -*- coding: utf-8 -*-

'''
Event Data API: Messages

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# apptools
from apptools import rpc
from apptools import model

# messages
from api.messages import edge

# event models
from api.models.tracker import event


## EventQuery
# Holds query parameters for an :py:class:`EventRange` query.
class EventQuery(rpc.messages.Message):

    ''' Query events by properties like start/end range,
        and tracker ID. Allows arbitrary filters. '''

    class TimewindowFilter(rpc.messages.Enum):

        ''' Enumerates available timewindows to filter
            on. '''

        HOURLY = 0x0  # return data by hour, clipped to start/end times
        FOREVER = 0x1  # return data for alltime, ignoring time filtering

    class QueryOptions(rpc.messages.Message):

        ''' Enumerates options that can be added to a
            :py:class:`EventQuery`. '''

        keys_only = rpc.messages.BooleanField(1, default=False)
        ancestor = rpc.messages.MessageField(model.Key.to_message_model(), 2)
        limit = rpc.messages.IntegerField(3, default=0)
        offset = rpc.messages.IntegerField(4, default=0)
        projection = rpc.messages.StringField(5, repeated=True)
        cursor = rpc.messages.StringField(6)

    class SortDirective(rpc.messages.Message):

        ''' Directs the query engine to sort results
            according to an arbitrary tuple of
            ``(property, direction)``. '''

        class SortOperator(rpc.messages.Enum):

            ''' Enumerates direction options (``ASC`` and ``DSC``)
                for sort directives part of an :py:class:`EventQuery`. '''

            ASCENDING = 0
            DESCENDING = 1

        property = rpc.messages.StringField(1, required=True)
        operator = rpc.messages.EnumField(SortOperator, 2, default=SortOperator.ASCENDING)

    class FilterDirective(rpc.messages.Message):

        ''' Directs the query engine to filter results with
            an arbitrary tuple of ``(property, operator, value)``. '''

        class FilterOperator(rpc.messages.Enum):

            ''' Enumerates operators allowed in a filter statement,
                as part of a :py:class:`FilterDirective` embedded
                in a :py:class:`EventQuery`. '''

            EQUALS = 0
            NOT_EQUALS = 1
            GREATER_THAN = 2
            GREATER_THAN_EQUAL_TO = 3
            LESS_THAN = 4
            LESS_THAN_EQUAL_TO = 5
            IN = 6

        property = rpc.messages.StringField(1, required=True)
        operator = rpc.messages.EnumField(FilterOperator, 2, default=FilterOperator.EQUALS)
        value = rpc.messages.VariantField(3, required=True)

    # builtin query parameters
    owner = rpc.messages.StringField(1)
    ref = rpc.messages.StringField(2)
    level = rpc.messages.IntegerField(3)

    # timewindow filtering
    start = rpc.messages.IntegerField(4)
    end = rpc.messages.IntegerField(5)
    scope = rpc.messages.EnumField(TimewindowFilter, 6, default=TimewindowFilter.HOURLY)

    # query directives + options
    sort = rpc.messages.MessageField(SortDirective, 7, repeated=True)
    filter = rpc.messages.MessageField(FilterDirective, 8, repeated=True)
    options = rpc.messages.MessageField(QueryOptions, 9)


## EventKeys
# Holds multiple keys for :py:class:`event.TrackedEvent` models.
class EventKeys(rpc.messages.Message):

    ''' Holds multiple keys for :py:class:`event.TrackedEvent`
        models. '''

    count = rpc.messages.IntegerField(1)
    keys = rpc.messages.MessageField(model.Key.to_message_model(), 2, repeated=True)
    range = rpc.messages.IntegerField(3, repeated=True)  # 2-member array of timestamp ints, like: ``[start, end]``


## EventRange
# Expresses a request for a range of :py:class:`event.TrackedEvent` models.
class EventRange(rpc.messages.Message):

    ''' Expresses a range of requested :py:class:`event.TrackedEvent`
        models, either as a request or a response. '''

    # range data
    start = rpc.messages.IntegerField(1)
    end = rpc.messages.IntegerField(2)
    data = rpc.messages.MessageField(event.TrackedEvent.to_message_model(), 3, repeated=True)

    # edges
    aggregations = rpc.messages.MessageField(edge.AggregationGroup, 4, repeated=True)
    attributions = rpc.messages.MessageField(edge.AttributionGroup, 5, repeated=True)


## Events
# Container for a set of related :py:class:`event.TrackedEvent` entities.
class Events(rpc.messages.Message):

    ''' Container for expressing multiple :py:class:`event.TrackedEvent`
        entities. '''

    pass
