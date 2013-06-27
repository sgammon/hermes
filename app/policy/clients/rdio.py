# -*- coding: utf -8 -*-

'''
Policy: Rdio

Event policy for Rdio.

:author: Leo Celis (leo.celis@ampush.com)
:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# policy imports
from policy import base
from protocol import decorators


## Rdio
# Legacy event profile for Rdio-owned trackers.
@decorators.legacy(ref='rdio')
class Rdio(base.LegacyProfile):

    ''' Legacy event tracking profile for trackers
        owned by Rdio. '''

    pass
