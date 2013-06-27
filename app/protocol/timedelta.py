# -*- coding: utf-8 -*-

"""
Protocol: Timedelta Bindings

Defines and enumerates available timedelta windows
and ancellary support bindings.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# meta protocol
from . import meta


# Globals
_GLOBAL_WINDOW_POSTFIX = '__global__'


## TimeWindow
# Specifies supported aggregation/attribution time windows.
class TimeWindow(meta.ProtocolDefinition):

    ''' Enumerates available timewindows for aggregation
        and attribution of properties/values. '''

    # Day Window
    ONE_DAY = 0x1

    # Hour-level Windows
    ONE_HOUR = 0x3
    TWO_HOURS = 0x4
    THREE_HOURS = 0x5
    FOUR_HOURS = 0x6
    FIVE_HOURS = 0x7
    SIX_HOURS = 0x8

    # Week-level Windows
    ONE_WEEK = 0x9
    TWO_WEEKS = 0xA
    THREE_WEEKS = 0xB
    FOUR_WEEKS = 0xC
    FIVE_WEEKS = 0xD
    SIX_WEEKS = 0xE

    # Month-level Windows
    MONTH = 0xF
    TWO_MONTHS = 0x10
    THREE_MONTHS = 0x11
    FOUR_MONTHS = 0x12
    FIVE_MONTHS = 0x13
    SIX_MONTHS = 0x14

    # Special Windows
    YEAR = 0x15
    FOREVER = 0x0
