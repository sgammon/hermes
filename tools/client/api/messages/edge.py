from protorpc import message_types
from apptools import rpc
from protorpc import messages
package = 'api.messages.edge'


class Aggregation(messages.Message):

  value = rpc.messages.VariantField(1)
  window = rpc.messages.VariantField(2, variant=messages.Variant.MESSAGE)
  multiplier = rpc.messages.VariantField(3, variant=messages.Variant.INT64, default='1')


class AggregationGroup(messages.Message):

  name = rpc.messages.VariantField(1)
  dimensions = rpc.messages.VariantField(2, repeated=True, variant=messages.Variant.MESSAGE)
  value = rpc.messages.VariantField(3, variant=messages.Variant.MESSAGE)


class AggregationValue(messages.Message):

  origin = rpc.messages.VariantField(1, variant=messages.Variant.MESSAGE)
  auxilliary = rpc.messages.VariantField(2, repeated=True, variant=messages.Variant.MESSAGE)


class Attribution(messages.Message):

  pass


class AttributionGroup(messages.Message):

  pass


class PropertyValue(messages.Message):

  property = rpc.messages.VariantField(1, required=True)
  value = rpc.messages.VariantField(2, required=True)


class Timewindow(messages.Message):


  class WindowScope(messages.Enum):

    FOREVER = 0
    HOUR = 1
    DAY = 2
    WEEK = 4
    MONTH = 5
    YEAR = 6

  scope = rpc.messages.VariantField(1, variant=messages.Variant.ENUM)
  delta = rpc.messages.VariantField(2, variant=messages.Variant.INT64)
  start = rpc.messages.VariantField(3, variant=messages.Variant.INT64)
  end = rpc.messages.VariantField(4, variant=messages.Variant.INT64)
