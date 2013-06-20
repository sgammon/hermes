# -*- coding: utf -8 -*-

'''
Policy: Amazon
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


class Amazon(base_clients.BaseClients):

    ''' Base profile for Amazon. '''

    refcode = frozenset(['amazon'])

    class Order(parameter.ParameterGroup):

        ''' More params. '''
        user_id = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'uid',
            'source': http.DataSlot.PARAM
        }

        event_name = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'event',
            'source': http.DataSlot.PARAM
        }

        conversion_type = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'convtype',
            'source': http.DataSlot.PARAM
        }

    class SignatureVerification(parameter.ParameterGroup):

        ''' More params. '''

        signature = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'signature',
            'source': http.DataSlot.PARAM
        }
