# -*- coding: utf -8 -*-

'''
Policy: Red Frog Events

Event policy suite for campaigns/conversion schemes owned
by Red Frog Events.

:author: Leo Celis (leo.celis@ampush.com)
:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# policy imports
from policy import base
from protocol import decorators


## Firefly
# Legacy event profile for trackers owned by Firefly.
@decorators.legacy(ref='firefly')
class Firefly(base.LegacyProfile):

    ''' Tracking policy for legacy hits owned by Firefly. '''

    pass


## IlluminiteRun
# Legacy event policy for trackers owned by Illuminite Run.
@decorators.legacy(ref='illuminite')
class IlluminiteRun(base.LegacyProfile):

    ''' Legacy policy for events owned by Illuminite Run. '''

    pass


## WarriorDash
# Legacy event tracking profile for Warrior Dash-owned trackers.
@decorators.legacy(ref='warriordash')
class WarriorDash(base.LegacyProfile):

    ''' Legacy tracking profile for Warrior Dash trackers. '''

    pass
