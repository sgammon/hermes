from protorpc import message_types
from apptools import rpc
from protorpc import messages
package = 'core'


class Key(messages.Message):
  
  id = rpc.VariantField(1)
  kind = rpc.VariantField(2)
  encoded = rpc.VariantField(3)
