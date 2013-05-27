# -*- coding: utf-8 -*-

'''
Contains models used in the `EventTracker` subsystem that are related to
expressing configuration and parameter profiles for Trackers.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# apptools models
from apptools import model

# hermes models
from api.models import client


## Profile
# Represents a profile that may be applied to `Tracker`(s) of events.
class Profile(model.Model):

    ''' Bundle of configuration for a `Tracker`. '''

    # == Metadata == #  # @TODO: Change str types to full enums.
    name = basestring, {'required': True, 'indexed': True}  # profile shortname for use in URLs/keys
    label = basestring, {'required': True, 'indexed': True}  # profile longname for use in UI/reporting
    scope = client.Contract, {'default': None, 'indexed': True}  # scoped owner of this profile
