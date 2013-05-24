# -*- coding: utf-8 -*-

'''
Holds model classes designed to express calculated ad attributions.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# apptools models
from apptools import model


## Attribution
# Represents a single attribution between an event and another event or datapoint.
class Attribution(model.Model):

    ''' Represents a single attribution from event=>event or event=>datapoint. '''

    pass


## AttributionGroup
# Represents a group of attributed events.
class AttributionGroup(model.Model):

    ''' Represents a group of bucketed, attributed events. '''

    name = basestring
    hashkey = basestring, {'repeated': True, 'indexed': True}
