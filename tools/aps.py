from protorpc import message_types
from apptools import services
from protorpc import messages
from protorpc import remote
package = 'tracker'


class Echo(messages.Message):
  message = services.VariantField(1)

class Input(messages.Message):
  
  accounts = services.VariantField(1)
  stimestamp = services.VariantField(2)
  etimestamp = services.VariantField(3)
  metrics = services.VariantField(4)


class Output(messages.Message):
  
  json = services.VariantField(1)


class APSService(remote.Service):
  
  @remote.method('aps.Input', 'aps.Output')
  def read(self, request):
    raise NotImplementedError('Method echo is not implemented')

  @remote.method('aps.Echo', 'aps.Echo')
  def read2(self, request):
    raise NotImplementedError('Method echo is not implemented')
