# -*- coding: utf -8 -*-

'''
Policy: State Farm

Event policy suite for State Farm.

:author: Leo Celis (leo.celis@ampush.com)
:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# policy imports
from policy import base
from protocol import decorators


## StateFarm
# Legacy tracking profile for State Farm-owned trackers.
@decorators.legacy(ref=frozenset(['statefarmrec', 'statefarmauto']))
class StateFarm(base.LegacyProfile):

    ''' Legacy event tracking profile for State Farm. '''

    pass
