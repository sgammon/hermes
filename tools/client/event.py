from protorpc import message_types
from apptools import rpc
from protorpc import messages
from protorpc import remote
from messages import rpc as struct
from messages import models
from messages import event
package = 'event'


class SortOperator(messages.Enum):

  ASCENDING = 0
  DESCENDING = 1


class FilterOperator(messages.Enum):

  EQUALS = 0
  NOT_EQUALS = 1
  GREATER_THAN = 2
  GREATER_THAN_EQUAL_TO = 3
  LESS_THAN = 4
  LESS_THAN_EQUAL_TO = 5
  IN = 6


class EventDataService(rpc.Service):

  @remote.method(struct.Key, models.TrackedEvent)
  def get(self, request):
    raise NotImplementedError('Method get is not implemented')

  @remote.method(event.EventKeys, event.Events)
  def get_multi(self, request):
    raise NotImplementedError('Method get_multi is not implemented')

  @remote.method(event.EventRange, event.Events)
  def get_range(self, request):
    raise NotImplementedError('Method get_range is not implemented')

  @remote.method(event.EventQuery, event.EventRange)
  def query(self, request):
    raise NotImplementedError('Method query is not implemented')
