# -*- coding: utf-8 -*-

'''

Tracker Models: Profiles

Contains models used in the `EventTracker` subsystem that are related to
expressing configuration and parameter profiles for Trackers.

-sam (<sam.gammon@ampush.com>)

'''

# stdlib
import time
import datetime

# apptools models
from apptools import model

# hermes models
from api.models import client
from api.models.tracker import integration
from api.models.tracker import attribution
from api.models.tracker import aggregation

# tracker protocol
from components.protocol import event


## TrackerProfile
# Represents a profile that may be applied to `Tracker`(s) of events.
class TrackerProfile(model.Model):

	''' Bundle of configuration for a `Tracker`. '''

	# == Metadata == #
	name = basestring, {'required': True, 'indexed': True}  # profile shortname for use in URLs/keys
	label = basestring, {'required': True, 'indexed': True}  # profile longname for use in UI/reporting
	scope = client.Contract, {'default': None, 'indexed': True}  # scoped owner of this profile: can be client/contract/ad/etc (attributed automatically)
	type = event.EventType, {'default': event.EventType.CUSTOM, 'indexed': True}  # type to apply to profile events
	provider = event.EventProvider, {'default': event.EventProvider.CLIENT, 'indexed': True}  # provider for events that match this profile

	# == Parameter Schema == #
	inherit = model.Key, {'repeated': True, 'indexed': True}  # super-schema to inherit from when calculating compound profile
	schema = param.Parameter, {'repeated': True, 'indexed': True}  # schema that is specific to this profile

	# == Integration Schema == #
	integrations = integration.Integration, {'repeated': True, 'indexed': True}  # linked integrations that must be dispatched when an event matches this profile
	aggregations = aggregation.AggregationGroup, {'repeated': True, 'indexed': True}  # aggregations that should be calculated when an event matches this profile
	attributions = attribution.AttributionGroup, {'repeated': True, 'indexed': True}  # attributions that should be calculated when an event matches this profile
