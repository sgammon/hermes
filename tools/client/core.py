from protorpc import message_types
from apptools import services
from protorpc import messages
package = 'core'


class Key(messages.Message):
  
  id = services.VariantField(1)
  kind = services.VariantField(2)
  encoded = services.VariantField(3)
