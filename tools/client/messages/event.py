from protorpc import message_types
from apptools import rpc
from protorpc import messages
from protorpc import remote
from . import raw, rpc as struct
from . import models, edge
package = 'messages.event'


class EventQuery(rpc.messages.Message):

    class QueryOptions(rpc.messages.Message):

        keys_only = rpc.messages.BooleanField(1, default=False)
        ancestor = rpc.messages.MessageField(struct.Key, 2)
        limit = rpc.messages.IntegerField(3, default=0)
        offset = rpc.messages.IntegerField(4, default=0)
        projection = rpc.messages.StringField(5, repeated=True)
        cursor = rpc.messages.StringField(6)

    class SortDirective(rpc.messages.Message):

        class SortOperator(rpc.messages.Enum):

            ASCENDING = 0
            DESCENDING = 1

        property = rpc.messages.StringField(1, required=True)
        operator = rpc.messages.EnumField(SortOperator, 2, default=SortOperator.ASCENDING)

    class FilterDirective(rpc.messages.Message):

        class FilterOperator(rpc.messages.Enum):

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
    start = rpc.messages.IntegerField(4)
    end = rpc.messages.IntegerField(5)
    scope = rpc.messages.EnumField(edge.Timewindow.WindowScope, 6, default=edge.Timewindow.WindowScope.HOUR)

    # query directives + options
    sort = rpc.messages.MessageField(SortDirective, 7, repeated=True)
    filter = rpc.messages.MessageField(FilterDirective, 8, repeated=True)
    options = rpc.messages.MessageField(QueryOptions, 9)


class EventKeys(rpc.messages.Message):

    count = rpc.messages.IntegerField(1)
    keys = rpc.messages.MessageField(struct.Key, 2, repeated=True)
    range = rpc.messages.IntegerField(3, repeated=True)  # 2-member array of timestamp ints, like: ``[start, end]``


class EventRange(rpc.messages.Message):

    start = rpc.messages.IntegerField(1)
    end = rpc.messages.IntegerField(2)
    data = rpc.messages.MessageField(models.TrackedEvent, 3, repeated=True)
    aggregations = rpc.messages.MessageField(edge.AggregationGroup, 4, repeated=True)
    attributions = rpc.messages.MessageField(edge.AttributionGroup, 5, repeated=True)


class Events(rpc.messages.Message):

    pass
