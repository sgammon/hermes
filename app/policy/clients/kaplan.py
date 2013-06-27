# -*- coding: utf -8 -*-

'''
Policy: Kaplan University

Event policy suite for Kaplan.

:author: Leo Celis (leo.celis@ampush.com)
:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# policy imports
from policy import base
from protocol import decorators


## Kaplan
# Legacy policy class for Kaplan-owned trackers.
@decorators.legacy(ref='kaplanu')
class Kaplan(base.LegacyProfile):

    ''' Legacy event policy for trackers owned by Kaplan. '''

    pass
