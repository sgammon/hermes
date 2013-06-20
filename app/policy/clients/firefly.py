# -*- coding: utf -8 -*-

'''
Policy: Firefly
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


class Firefly(base_clients.BaseClients):

    refcode = frozenset(['firefly'])
