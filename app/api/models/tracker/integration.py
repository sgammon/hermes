# -*- coding: utf-8 -*-

'''
Contains models used in the `EventTracker` subsystem that are related to
expressing configuration and audit for integrated systems.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# stdlib
import time
import datetime

# apptools models
from apptools import model


## Integration
# Represents an external system integrated with `EventTracker`.
class Integration(model.Model):

    ''' An external system integrated with `EventTracker`. '''

    ## == Metadata == ##
    name = basestring, {'required': True, 'indexed': True}  # shotname for use in URLs and keys
    label = basestring, {'required': True, 'indexed': False}  # longname label for UI/reporting


## Routine
# Represents a code-based routine for fulfilling an integration.
class Routine(model.Model):

    ''' A defined action linked to an `Integration` which provides code bindings. '''

    ## == Metadata == ##
    name = basestring, {'required': True, 'indexed': True}  # shortname for use in URLs and keys
    label = basestring, {'required': True, 'indexed': False}  # longname label for UI/reporting

    ## == Dispatch Config == ##
    external = bool, {'default': False, 'indexed': True}  # whether this action was performed externally
    codepath = basestring, {'required': True, 'indexed': False}  # path to code to dispatch for this `Routine`

    ## == Linked Objects == ##
    integration = Integration, {'required': True, 'indexed': True}  # linked integration provider
