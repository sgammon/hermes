# -*- coding: utf -8 -*-

'''
Policy: Snorg Tees

Event policy suite for SnorgTees.

:author: Leo Celis (leo.celis@ampush.com)
:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# policy imports
from policy import base
from protocol import decorators


## SnorgTees
# Legacy event profile for trackers owned by SnorgTees.
@decorators.legacy(ref='snorgtees')
class SnorgTees(base.LegacyProfile):

    ''' Legacy tracking profile for trackers owned by SnorgTees. '''

    pass
