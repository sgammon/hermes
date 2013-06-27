# -*- coding: utf -8 -*-

'''
Policy: DegreeLeap

Event policy suite for DegreeLeap.

:author: Leo Celis (leo.celis@ampush.com)
:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# policy imports
from policy import base
from protocol import decorators


## DegreeLeap
# Legacy profile class for trackers owned by Degree Leap.
@decorators.legacy(ref='degreeleap')
class DegreeLeap(base.LegacyProfile):

    ''' Legacy event policy for trackers owned by Degree Leap. '''

    pass
