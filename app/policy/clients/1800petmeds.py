# -*- coding: utf -8 -*-

'''
Policy: 1800-PetMeds
'''

# base clients
from policy import base

# protocol imports
from protocol import http
from protocol import parameter


## PetMeds
# Legacy event policy class for trackers owned by 1800-Pet-Meds.
class PetMeds(base.LegacyProfile):

    ''' Legacy event profile for 1800 Pet Meds. '''

    refcode = '800petmeds'

    class Order(parameter.ParameterGroup):

        revenue = float, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'spent',
            'source': http.DataSlot.PARAM
        }
