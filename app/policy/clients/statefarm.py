# -*- coding: utf -8 -*-

'''
Policy: State Farm
'''

# policy imports
from policy import base

# protocol imports
from protocol import http
from protocol import parameter


## StateFarm
# Legacy tracking profile for State Farm-owned trackers.
class StateFarm(base.LegacyProfile):

    ''' Legacy event tracking profile for State Farm. '''

    refcode = frozenset(['statefarmrec', 'statefarmauto'])
