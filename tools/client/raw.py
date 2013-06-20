from protorpc import message_types
from apptools import rpc
from protorpc import messages
from protorpc import remote
from messages import rpc as struct
from messages import raw, models
package = 'raw'


class RawDataService(rpc.Service):

  @remote.method(struct.Key, models.Event)
  def get(self, request):
    raise NotImplementedError('Method get is not implemented')

  @remote.method(message_types.VoidMessage, raw.RawEvents)
  def get_all(self, request):
    raise NotImplementedError('Method get_all is not implemented')

  @remote.method(raw.RawKeys, raw.RawEvents)
  def get_multi(self, request):
    raise NotImplementedError('Method get_multi is not implemented')
