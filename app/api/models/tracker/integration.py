# -*- coding: utf-8 -*-

'''

Tracker Models: Integration

Contains models used in the `EventTracker` subsystem that are related to
expressing configuration and audit for integrated systems.

-sam (<sam.gammon@ampush.com>)

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
