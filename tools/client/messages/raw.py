from protorpc import message_types
from apptools import rpc
from protorpc import messages
from protorpc import remote
from . import models, rpc as struct
package = 'messages.raw'


class RawKeys(rpc.messages.Message):

    keys = rpc.messages.MessageField(struct.Key, 1, repeated=True)


class RawEvents(rpc.messages.Message):

    count = rpc.messages.IntegerField(1)
    events = rpc.messages.MessageField(models.Event, 2, repeated=True)
