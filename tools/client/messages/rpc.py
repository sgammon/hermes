from protorpc import message_types
from apptools import rpc
from protorpc import messages
from protorpc import remote

package = 'messages.rpc'


class Echo(messages.Message):

  message = rpc.messages.VariantField(1, default='Hello, world!')


class Key(messages.Message):

  encoded = rpc.messages.VariantField(1)
  kind = rpc.messages.VariantField(2)
  id = rpc.messages.VariantField(3)
  namespace = rpc.messages.VariantField(4)
  parent = rpc.messages.VariantField(5, variant=messages.Variant.MESSAGE)
