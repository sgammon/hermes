# -*- coding: utf -8 -*-

'''
Policy: DegreeLeap
'''

# base clients
from policy.clients import base_clients

# protocol imports
from protocol import http
from protocol import parameter


## DegreeLeap
# Legacy profile class for trackers owned by Degree Leap.
class DegreeLeap(base_clients.BaseClients):

    ''' Legacy event policy for trackers owned by Degree Leap. '''

    refcode = frozenset(['degreeleap'])

    class Order(parameter.ParameterGroup):

        revenue = float, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'spent',
            'source': http.DataSlot.PARAM
        }
