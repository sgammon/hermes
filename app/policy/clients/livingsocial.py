# -*- coding: utf -8 -*-

'''
Policy: LivingSocial
'''

# policy imports
from policy.clients import base_clients

# protocol imports
from protocol import meta
from protocol import http
from protocol import parameter
from protocol import timedelta
from protocol import aggregation
from protocol.decorators import param


class LivingSocial(base_clients.BaseClients):

    ''' Base profile for LivingSocial. '''
    refcode = frozenset(['livingsocialUS',
                         'livingsocialUSstory'])

    class Order(parameter.ParameterGroup):

        user_id = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'uid',
            'source': http.DataSlot.PARAM
        }

        order = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'unique',
            'source': http.DataSlot.PARAM
        }

        deal = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'deal_id',
            'source': http.DataSlot.PARAM
        }

        reference_code = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'ref_code',
            'source': http.DataSlot.PARAM
        }

        revenue = float, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'spent',
            'source': http.DataSlot.PARAM
        }
