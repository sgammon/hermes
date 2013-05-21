# -*- coding: utf-8 -*-

'''
Contains models used to model and express parameters/args linked
to `TrackedEvent` or `Profile`/`Tracker` objects.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# apptools models
from apptools import model


## Parameter
# Represents a parameter that may be present as part of a `TrackedEvent`.
class Parameter(model.Model):

    ''' Profile for a parameter (linked to a `Profile`) that may be present in a `TrackedEvent`. '''

    # == Metadata == #
    name = basestring, {'required': True, 'indexed': True}  # profile shortname for use in URLs/keys
    label = basestring, {'required': True, 'indexed': True}  # profile longname for use in UI/reporting

    # == Field/Value Information == #  # @TODO: Change strings to full enum types.
    policy = str, {'default': 'OPTIONAL', 'indexed': True}  # default to an optional param
    basetype = str, {'default': 'STRING', 'indexed': True}  # map basetype for parameter value
