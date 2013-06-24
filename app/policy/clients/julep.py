# -*- coding: utf -8 -*-

'''
Policy: Julep
'''

# base clients
from policy import base


## Julep
# Legacy event profile for Rdio-owned trackers.
class Julep(base.LegacyProfile):

    ''' Legacy event tracking profile for trackers
        owned by Julep. '''

    refcode = 'julep'
