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


## AttributionGroup
class AttributionGroup(model.Model):

    ''' Represents a group of bucketed, attributed events. '''

    name = basestring, {'indexed': False}
    hash = basestring, {'indexed': True}
    hashkey = basestring, {'repeated': True, 'indexed': False}
    cookie = bool, {'default': True}
    param = basestring
    target = basestring, {'repeated': True}


## Attribution
class Attribution(model.Model):

    ''' Represents a single attribution from event=>event or event=>datapoint. '''

    resolved = bool, {'indexed': True, 'default': False}
    group = AttributionGroup, {'required': True, 'indexed': True}
