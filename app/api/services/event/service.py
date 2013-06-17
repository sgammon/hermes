# -*- coding: utf-8 -*-

'''
Event Data API: Service

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# stdlib
import datetime

# Local Imports
from . import messages
from . import exceptions

# apptools rpc
from apptools import rpc
from apptools import model

# API messages
from api.messages import edge

# API Models
from api.models.tracker import event


## Globals
Direction = messages.EventQuery.SortDirective.SortOperator
Operator = messages.EventQuery.FilterDirective.FilterOperator


## EventDataService - exposes methods for extracting data from `EventTracker`.
@rpc.service
class EventDataService(rpc.Service):

    ''' Exposes methods for interacting with & extracting data from `EventTracker`. '''

    name = 'event'
    _config_path = 'hermes.api.tracker.EventDataAPI'

    exceptions = rpc.Exceptions(**{
        'generic': exceptions.Error
    })

    @rpc.method(model.Key, event.TrackedEvent)
    def get(self, request):

        ''' Retrieve a :py:class:`event.TrackedEvent` model
            by its associated :py:class:`model.Key`. '''

        pass

    @rpc.method(messages.EventKeys, messages.Events)
    def get_multi(self, request):

        ''' Retrieve multiple :py:class:`event.TrackedEvent`
            models by their associated :py:class:`model.Key`
            objects. '''

        pass

    @rpc.method(messages.EventRange, messages.Events)
    def get_range(self, request):

        ''' Retrieve a range of :py:class:`event.TrackedEvent`
            models by special values attached to them. '''

        pass

    @rpc.method(messages.EventQuery, messages.EventRange)
    def query(self, request):

        ''' Execute a compound/arbitrary query across
            :py:class:`event.TrackedEvent` records,
            returning matching results. '''

        # start building a query
        q = event.TrackedEvent.query(**{
            'keys_only': request.options.keys_only,
            'ancestor': request.options.ancestor,
            'limit': request.options.limit,
            'offset': request.options.offset,
            'projection': request.options.projection,
            'cursor': request.options.cursor
        })

        # filter by tracker, if specified
        if request.tracker:
            q.filter(event.TrackedEvent.tracker == request.tracker)

        # build start and end ranges
        if request.start:
            timestamp_start = int(request.start / 1e3) if len(str(request.start)) > 10 else request.start
            q.filter(event.TrackedEvent.created > datetime.datetime.fromtimestamp(timestamp_start))

        if request.end:
            timestamp_end = int(request.end / 1e3) if len(str(request.end)) > 10 else request.end
            q.filter(event.TrackedEvent.created < datetime.datetime.fromtimestamp(timestamp_end))

        # add arbitrary filter directives
        if request.filter:
            for directive in request.filters:

                # `==` filter
                if directive.operator is Operator.EQUALS:
                    q.filter(event.TrackedEvent[directive.property] == directive.value)

                # `!=` filter
                elif directive.operator is Operator.NOT_EQUALS:
                    q.filter(event.TrackedEvent[directive.property] != directive.value)

                # `<` filter
                elif directive.operator is Operator.LESS_THAN:
                    q.filter(event.TrackedEvent[directive.property] < directive.value)

                # `<=` filter
                elif directive.operator is Operator.LESS_THAN_EQUAL_TO:
                    q.filter(event.TrackedEvent[directive.property] <= directive.value)

                # `>` filter
                elif directive.operator is Operator.GREATER_THAN:
                    q.filter(event.TrackedEvent[directive.property] > directive.value)

                # `>=` filter
                elif directive.operator is Operator.GREATER_THAN_EQUAL_TO:
                    q.filter(event.TrackedEvent[directive.property] >= directive.value)

                # `IN` filter
                elif directive.operator is Operator.IN:
                    q.filter(event.TrackedEvent[directive.property] in directive.value)

        # add arbitrary sort directives
        if request.sort:
            for directive in request.sort:

                # ascending sort
                if directive.operator is Direction.ASCENDING:
                    q.sort(+event.TrackedEvent[directive.property])

                # descending sort
                if directive.operator is Direction.DESCENDING:
                    q.sort(-event.TrackedEvent[directive.property])

        results = q.fetch()  # fetch results
        import pdb; pdb.set_trace()

        # initialize results containers
        _matched_aggregations = set()
        _matched_attributions = set()

        edges, event_data = {
            'aggregations': [],
            'attributions': []
        }, []

        for event in results:

            # build unique set of aggregations to pull
            if event.aggregations:
                for aggregation in event.aggregations:
                    if aggregation not in _matched_aggregations:
                        _matched_aggregations.add(aggregation)

            # build unique set of attribution groups to pull
            if event.attributions:
                for attribution in event.attributions:
                    if attribution not in _matched_attributions:
                        _matched_attributions.add(attribution)

        # pull aggregated values
        if len(_matched_aggregations):
            for matched_aggregation in _matched_aggregations:

                # split aggregation key and extract metadata
                match_split = matched_aggregation.split(self.tracker.engine._magic_separator)
                path, window, identifier = match_split[1:-2], match_split[-2], match_split[-1]

                # grab value, calculate window
                value = self.tracker.engine.read_counter(matched_aggregation)
                window, trange = self.tracker.engine.resolve_timewindow(window, identifier)

                @@@@@@@@@ RESOLVE TIMEWINDOW @@@@@@@@@@

                edges['aggregations'].append(edge.Aggregation(**{
                    'value': value,
                }))

        return messages.EventRange(**{
            'start': timestamp_start,
            'end': timestamp_end,
            'data': event_data,
            'aggregations': edges['aggregations'],
            'attributions': edges['attributions']
        })
