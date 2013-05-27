from protorpc import message_types
from apptools import rpc
from protorpc import messages
from protorpc import remote
package = 'tracker'


class Echo(messages.Message):
  
  key = rpc.VariantField(1, variant=messages.Variant.MESSAGE)
  message = rpc.VariantField(2, default='Hello, world!')


class TrackerService(remote.Service):
  
  @remote.method('tracker.Echo', 'tracker.Echo')
  def echo(self, request):
    raise NotImplementedError('Method echo is not implemented')
