# -*- coding: utf-8 -*-

'''
Event Data API: Service

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# stdlib
import time
import base64
import datetime

# Local Imports
from . import messages
from . import exceptions

# apptools rpc
from apptools import rpc

# apptools models
from apptools import model
from apptools.model import query

# API messages
from api.messages import edge

# API Models
from api.models.tracker import endpoint
from api.models.tracker.event import TrackedEvent


## Globals
Direction = messages.EventQuery.SortDirective.SortOperator
Operator = messages.EventQuery.FilterDirective.FilterOperator


## EventDataService - exposes methods for extracting data from `EventTracker`.
@rpc.service(name='event')
class EventDataService(rpc.Service):

    ''' Exposes methods for interacting with & extracting data from `EventTracker`. '''

    _config_path = 'hermes.api.tracker.EventDataAPI'

    exceptions = rpc.Exceptions(**{
        'generic': exceptions.Error,
        'invalid_query': exceptions.InvalidQuery,
        'invalid_owner': exceptions.InvalidOwner,
        'unknown_owner': exceptions.UnknownOwner,
        'invalid_timerange': exceptions.InvalidTimerange,
        'invalid_timewindow': exceptions.InvalidTimewindow
    })

    @staticmethod
    def _build_query(_opts, _queries):

        ''' Build a new query object, given a set of ``_opts``
            specified by a query submitted to the Event Data
            API. '''

        q = TrackedEvent.query(**{
            'keys_only': _opts.keys_only,
            'ancestor': _opts.ancestor,
            'limit': _opts.limit,
            'offset': _opts.offset,
            'projection': _opts.projection,
            'cursor': _opts.cursor
        })

        _queries.append(q)
        return q

    @rpc.method(model.Key, TrackedEvent)
    def get(self, request):

        ''' Retrieve a :py:class:`event.TrackedEvent` model
            by its associated :py:class:`model.Key`. '''

        raise self.exceptions.generic('Event Data API method `get` is not yet implemented.')

    @rpc.method(messages.EventKeys, messages.Events)
    def get_multi(self, request):

        ''' Retrieve multiple :py:class:`event.TrackedEvent`
            models by their associated :py:class:`model.Key`
            objects. '''

        raise self.exceptions.generic('Event Data API method `get_multi` is not yet implemented.')

    @rpc.method(messages.EventRange, messages.Events)
    def get_range(self, request):

        ''' Retrieve a range of :py:class:`event.TrackedEvent`
            models by special values attached to them. '''

        raise self.exceptions.generic('Event Data API method `get_range` is not yet implemented.')

    @rpc.method(messages.EventQuery, messages.EventRange)
    def query(self, request):

        ''' Execute a compound/arbitrary query across
            :py:class:`event.TrackedEvent` records,
            returning matching results. '''

        if not request.options:
            _opts = query.QueryOptions(keys_only=True)  # default to keys-only
        else:
            _opts = request.options

        # build initial results window and query
        _queries, _event_keys, _tracker_keys = [], [], []
        q = self._build_query(_opts, _queries)

        # filter by tracker, if specified
        if request.owner:

            ## try to pull trackers for this owner
            t = endpoint.Tracker.query(keys_only=True).filter(endpoint.Tracker.owner == request.owner)
            trackers = t.fetch()

            ## does this account have modern trackers provisioned?
            if trackers:
                ## @TODO(sgammon): implement support for modern trackers
                raise self.exceptions.invalid_owner('`EventService` method `query` does not yet support modern tracking.')
            else:
                raise self.exceptions.unknown_owner('Owner `%s` failed to resolve to a valid Tracker.' % request.owner)

        # build start range
        if request.start:
            timestamp_start = int(request.start / 1e3) if len(str(request.start)) > 10 else request.start
            q.filter(TrackedEvent.created > datetime.datetime.fromtimestamp(timestamp_start))
        else:
            timestamp_start = None

        # build end range
        if request.end:
            timestamp_end = int(request.end / 1e3) if len(str(request.end)) > 10 else request.end
            q.filter(TrackedEvent.created < datetime.datetime.fromtimestamp(timestamp_end))
        else:
            timestamp_end = None

        # filter out invalid time ranges
        if timestamp_start > timestamp_end:
            raise self.exceptions.invalid_timerange('Invalid timerange: end time ("%s") cannot be less than the start time ("%s").' % (request.start, request.end))

        # add arbitrary filter directives
        if request.filter:
            for directive in request.filter:

                # `==` filter
                if directive.operator is Operator.EQUALS:
                    q.filter(TrackedEvent[directive.property] == directive.value)

                # `!=` filter
                elif directive.operator is Operator.NOT_EQUALS:
                    q.filter(TrackedEvent[directive.property] != directive.value)

                # `<` filter
                elif directive.operator is Operator.LESS_THAN:
                    q.filter(TrackedEvent[directive.property] < directive.value)

                # `<=` filter
                elif directive.operator is Operator.LESS_THAN_EQUAL_TO:
                    q.filter(TrackedEvent[directive.property] <= directive.value)

                # `>` filter
                elif directive.operator is Operator.GREATER_THAN:
                    q.filter(TrackedEvent[directive.property] > directive.value)

                # `>=` filter
                elif directive.operator is Operator.GREATER_THAN_EQUAL_TO:
                    q.filter(TrackedEvent[directive.property] >= directive.value)

                # `IN` filter
                elif directive.operator is Operator.IN:
                    q.filter(TrackedEvent[directive.property] in directive.value)

        # add arbitrary sort directives
        if request.sort:
            for directive in request.sort:

                # ascending sort
                if directive.operator is Direction.ASCENDING:
                    q.sort(+TrackedEvent[directive.property])

                # descending sort
                if directive.operator is Direction.DESCENDING:
                    q.sort(-TrackedEvent[directive.property])

        results = q.fetch()  # fetch results

        # initialize results containers
        _matched_aggregations, _touched_aggregations = set(), set()
        _matched_attributions, _touched_attributions = set(), set()

        edges, event_data, _aggr_raw, _attr_raw, _final = {
            'aggregations': {},
            'attributions': {}
        }, [], [], [], {}

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

                # extract name and data from path
                if len(path) > 1:
                    nm, data = path[0], path[1:]
                    main_value, auxilliary = (nm, data[0]), dict(zip(data[1::2], data[2::2])) if len(data) > 1 else {}
                else:
                    nm, data = path[0], []
                    main_value, auxilliary = None, {}

                aux = tuple(auxilliary.items())  # make lookup list of all pairs

                # grab value, calculate window
                wire_window, trange = self.tracker.resolve_timewindow(*(
                    window,
                    identifier,
                    edge.Timewindow.WindowScope
                ))

                window_type, window_delta = wire_window  # extract window values
                window_begin, window_end = trange  # extract beginning and end of window

                # initialize aggregation in hash, if we haven't seen it yet
                if (nm, (main_value, aux)) not in _touched_aggregations:
                    edges['aggregations'][(nm, (main_value, aux))] = []
                    _touched_aggregations.add((nm, (main_value, aux)))

                # generate aggregation item
                _directive = edge.Aggregation(**{
                    'window': edge.Timewindow(**{
                        'scope': window_type,
                        'delta': window_delta,
                        'start': int(time.mktime(window_begin.timetuple())) if window_begin else None,
                        'end': int(time.mktime(window_end.timetuple())) if window_end else None
                    })
                })

                _aggr_raw.append((matched_aggregation, _directive))
                edges['aggregations'][(nm, (main_value, aux))].append(_directive)

            # batch-get aggregation values
            aggregation_values = self.tracker.engine.get_multi((key for key, obj in _aggr_raw))

            # zip objects up with values and fill in results
            for obj, value in zip((obj for key, obj in _aggr_raw), aggregation_values):
                try:
                    if isinstance(value, basestring):
                        if '.' in value:
                            obj.value = float(value)
                        else:
                            obj.value = int(value)
                    else:
                        obj.value = value
                except ValueError:
                    try:
                        obj.value = int(value)
                    except ValueError:
                        obj.value = value

        # build eventrange result
        event_range = messages.EventRange(**{
            'start': timestamp_start,
            'end': timestamp_end,
            'data': event_data,
            'aggregations': [],
            'attributions': []
        })

        for k, v in edges['aggregations'].iteritems():

            # extract everything
            name, path = k
            origin, auxilliary = path
            origin_name, origin_value = origin

            # build property values
            origin_prop = edge.PropertyValue(**{
                'property': origin_name,
                'value': base64.b64decode(origin_value)
            })

            # build auxilliary props
            aux_prop = []
            for aux in auxilliary:
                aux_name, aux_value = aux
                aux_prop.append(edge.PropertyValue(**{
                    'property': aux_name,
                    'value': base64.b64decode(aux_value)
                }))

            # build aggregation group
            event_range.aggregations.append(edge.AggregationGroup(**{
                'name': name,
                'dimensions': v,
                'value': edge.AggregationValue(**{
                    'origin': origin_prop,
                    'auxilliary': aux_prop
                })
            }))

        # stub-out attributions for now
        for k, v in edges['attributions'].iteritems():
            raise self.exceptions.invalid_query('Attribution is not yet supported. '
                                                'Found %s matching hit attributions - failing.' % len(edges['attributions']))

        return event_range
