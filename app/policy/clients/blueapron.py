# -*- coding: utf -8 -*-

'''
Policy: Blue Apron
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


class BlueApron(base_clients.BaseClients):

    refcode = frozenset(['blueapron'])

    class Event(parameter.ParameterGroup):

        event_name = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'event',
            'source': http.DataSlot.PARAM
        }
