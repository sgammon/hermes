# -*- coding: utf-8 -*-

'''
Holds model classes designed to express aggregation groups and aggregations
linked to ``TrackedEvent``.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# apptools models
from apptools import model


## AggregationGroup
# Represents a group of aggregations linked to a value or `Tracker`/`Profile`.
class AggregationGroup(model.Model):

    ''' Represents a group of `Aggregation` objects linked to a `Tracker` or `Profile`. '''

    name = basestring, {'indexed': True}  # name of the property being aggregated
    basekind = basestring, {'indexed': True}  # name of the kind owning this property


## Aggregation
# Represents an aggregation "matched-to" a `TrackedEvent`.
class Aggregation(model.Model):

    ''' Represents a single aggregation match from an event=>property or event=>object. '''

    value = float, {'required': True, 'indexed': True}
    group = AggregationGroup, {'required': True, 'indexed': True}
