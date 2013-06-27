# -*- coding: utf -8 -*-

'''
Policy: myVEGAS

Event policy for myVEGAS.

:author: Leo Celis (leo.celis@ampush.com)
:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# policy imports
from policy import base
from protocol import decorators


## MyVegas
# Legacy event profile for trackers owned by MyVegas.
@decorators.legacy(ref='myvegas')
class MyVegas(base.LegacyProfile):

    ''' Legacy event profile for trackers owned by MyVegas. '''

    pass
