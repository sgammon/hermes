# -*- coding: utf-8 -*-

'''
Contains models used in the `EventTracker` subsystem that are related to
expressing configuration and parameter profiles for Trackers.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# stdlib
import datetime

# apptools models
from apptools import model

# hermes models
from api.models import client
from api.models.tracker import parameter
from api.models.tracker import integration
from api.models.tracker import attribution
from api.models.tracker import aggregation


## Profile
# Represents a profile that may be applied to `Tracker`(s) of events.
class Profile(model.Model):

    ''' Bundle of configuration for a `Tracker`. '''

    # == Metadata == #  # @TODO: Change str types to full enums.
    name = basestring, {'required': True, 'indexed': True}  # profile shortname for use in URLs/keys
    label = basestring, {'required': True, 'indexed': True}  # profile longname for use in UI/reporting
    scope = client.Contract, {'default': None, 'indexed': True}  # scoped owner of this profile: can be client/contract/ad/etc (attributed automatically)
    type = str, {'default': 'CUSTOM', 'indexed': True}  # type to apply to profile events
    provider = str, {'default': 'CLIENT', 'indexed': True}  # provider for events that match this profile

    # == Parameter Schema == #
    inherit = model.Key, {'repeated': True, 'indexed': True}  # super-schema to inherit from when calculating compound profile
    schema = parameter.Parameter, {'repeated': True, 'indexed': True}  # schema that is specific to this profile

    # == Integration Schema == #
    integrations = integration.Integration, {'repeated': True, 'indexed': True}  # linked integrations that must be dispatched when an event matches this profile
    aggregations = aggregation.AggregationGroup, {'repeated': True, 'indexed': True}  # aggregations that should be calculated when an event matches this profile
    attributions = attribution.AttributionGroup, {'repeated': True, 'indexed': True}  # attributions that should be calculated when an event matches this profile
