# -*- coding: utf -8 -*-

'''
Policy: Kaplan University
'''

# base clients
from policy.clients import base_clients


## Kaplan
# Legacy policy class for Kaplan-owned trackers.
class Kaplan(base_clients.BaseClients):

    ''' Legacy event policy for trackers owned by Kaplan. '''

    refcode = 'kaplanu'
