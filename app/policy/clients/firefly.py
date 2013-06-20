# -*- coding: utf -8 -*-

'''
Policy: Firefly
'''

# base clients
from policy import base


## Firefly
# Legacy event profile for trackers owned by Firefly.
class Firefly(base.LegacyProfile):

    ''' Tracking policy for legacy hits owned by Firefly. '''

    refcode = 'firefly'
