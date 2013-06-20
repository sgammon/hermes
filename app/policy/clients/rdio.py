# -*- coding: utf -8 -*-

'''
Policy: Rdio
'''

# base clients
from policy import base


## Rdio
# Legacy event profile for Rdio-owned trackers.
class Rdio(base.LegacyProfile):

    ''' Legacy event tracking profile for trackers
        owned by Rdio. '''

    refcode = 'rdio'
