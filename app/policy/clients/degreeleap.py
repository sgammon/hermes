# -*- coding: utf -8 -*-

'''
Policy: DegreeLeap
'''

# base clients
from policy.clients import base_clients

# protocol imports
from protocol import meta
from protocol import http
from protocol import parameter
from protocol import timedelta
from protocol import aggregation
from protocol.decorators import param


class DegreeLeap(base_clients.BaseClients):

    refcode = frozenset(['degreeleap'])

    class Order(parameter.ParameterGroup):

        revenue = float, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'spent',
            'source': http.DataSlot.PARAM
        }
