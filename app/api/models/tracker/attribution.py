# -*- coding: utf-8 -*-

'''

Tracker Models: Attribution

Holds model classes designed to express calculated ad attributions.

-sam (<sam.gammon@ampush.com>)

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

    pass
