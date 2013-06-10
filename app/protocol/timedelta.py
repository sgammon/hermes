# -*- coding: utf-8 -*-

'''

Timedelta Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# Protocol
from protocol import meta


# Globals
_GLOBAL_WINDOW_POSTFIX = '__global__'


## TimeWindow
# Specifies supported aggregation/attribution time windows.
class TimeWindow(meta.ProtocolDefinition):

    ''' Enumerates available timewindows for aggregation
        and attribution of properties/values. '''

    # Day Window
    ONE_DAY = 0x1

    # Week-level Windows
    ONE_WEEK = 0x2
    TWO_WEEKS = 0x3
    THREE_WEEKS = 0x4
    FOUR_WEEKS = 0x5
    FIVE_WEEKS = 0x6
    SIX_WEEKS = 0x7

    # Month-level Windows
    MONTH = 0x8
    TWO_MONTHS = 0x9
    THREE_MONTHS = 0xA
    FOUR_MONTHS = 0xB
    FIVE_MONTHS = 0xC
    SIX_MONTHS = 0xD

    # Special Windows
    YEAR = 0xF
    FOREVER = 0x0
