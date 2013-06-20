# -*- coding: utf -8 -*-

'''
Policy: Kaplan University
'''

# base clients
from policy import base


## Kaplan
# Legacy policy class for Kaplan-owned trackers.
class Kaplan(base.LegacyProfile):

    ''' Legacy event policy for trackers owned by Kaplan. '''

    refcode = 'kaplanu'
