# -*- coding: utf -8 -*-

'''
Policy: 1800-PetMeds
'''

# base clients
from policy.clients import base_clients

# protocol imports
from protocol import meta
from protocol import http
from protocol import parameter
from protocol import timedelta
from protocol import aggregation
from protocol.decorators import paramm


class PetMeds(base_clients.BaseClients):

    refcode = frozenset(['800petmeds'])

    class Order(parameter.ParameterGroup):

        revenue = float, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'spent',
            'source': http.DataSlot.PARAM
        }
