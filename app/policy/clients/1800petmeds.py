# -*- coding: utf -8 -*-

'''
Policy: 1800-PetMeds

Event policy suite for 1800-PetMeds.

:author: Leo Celis (leo.celis@ampush.com)
:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# policy imports
from policy import base
from protocol import decorators


## PetMeds
# Legacy event policy class for trackers owned by 1800-Pet-Meds.
@decorators.legacy(ref='800petmeds')
class PetMeds(base.LegacyProfile):

    ''' Legacy event profile for 1800 Pet Meds. '''

    pass
