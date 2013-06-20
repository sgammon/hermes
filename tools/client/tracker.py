from protorpc import message_types
from apptools import rpc
from protorpc import messages
from protorpc import remote
from messages import rpc as struct
from messages import models
package = 'tracker'


class TrackerService(rpc.Service):

  @remote.method(struct.Key, models.Tracker)
  def get(self, request):
    raise NotImplementedError('Method get is not implemented')

  @remote.method('messages.Profile', 'messages.Profile')
  def profile(self, request):
    raise NotImplementedError('Method profile is not implemented')

  @remote.method('messages.Profiles', 'messages.Profiles')
  def profiles(self, request):
    raise NotImplementedError('Method profiles is not implemented')

  @remote.method('messages.ProvisioningRequest', 'messages.TrackerSet')
  def provision(self, request):
    raise NotImplementedError('Method provision is not implemented')

  @remote.method(models.Tracker, models.Tracker)
  def put(self, request):
    raise NotImplementedError('Method put is not implemented')
