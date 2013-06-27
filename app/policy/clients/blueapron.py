# -*- coding: utf -8 -*-

'''
Policy: Blue Apron

Event policy suite for Blue Apron.

:author: Leo Celis (leo.celis@ampush.com)
:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# policy imports
from policy import base
from protocol import decorators


## BlueApron
# Policy class for trackers owned by Blue Apron.
@decorators.legacy(ref='blueapron')
class BlueApron(base.LegacyProfile):

    ''' Legacy event policy class for trackers owned
        by Blue Apron. '''

    pass
