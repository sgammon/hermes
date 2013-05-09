# -*- coding: utf-8 -*-

'''

Tracker Models: Aggregation

Holds model classes designed to express aggregation groups and aggregations
linked to `TrackedEvent`(s).

-sam (<sam.gammon@ampush.com>)

'''

# apptools models
from apptools import model


## Aggregation
# Represents an aggregation "matched-to" a `TrackedEvent`.
class Aggregation(model.Model):

	''' Represents a single aggregation match from an event=>property or event=>object. '''

	pass


## AggregationGroup
# Represents a group of aggregations linked to a value or `Tracker`/`Profile`.
class AggregationGroup(model.Model):

    ''' Represents a group of `Aggregation` objects linked to a `Tracker` or `Profile`. '''

    pass
