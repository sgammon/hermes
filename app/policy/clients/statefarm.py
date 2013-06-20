# -*- coding: utf -8 -*-

'''
Policy: State Farm
'''

# policy imports
from policy import base

# protocol imports
from protocol import http
from protocol import parameter


## StateFarm
# Legacy tracking profile for State Farm-owned trackers.
class StateFarm(base.LegacyProfile):

    ''' Legacy event tracking profile for State Farm. '''

    refcode = frozenset(['statefarmrec', 'statefarmauto'])

    class ConversionLevel(parameter.ParameterGroup):

        ''' Sample property we're adding to the profile. '''

        level1 = bool, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'source': http.DataSlot.PARAM,
            'name': ('conv1', 'c1')
        }

        level2 = bool, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'source': http.DataSlot.PARAM,
            'name': 'conv2'
        }

        level3 = bool, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'source': http.DataSlot.PARAM,
            'name': 'conv3'
        }

        level4 = bool, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'source': http.DataSlot.PARAM,
            'name': 'conv4'
        }

        revenue = float, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'source': http.DataSlot.PARAM,
            'name': 'revenue'
        }
