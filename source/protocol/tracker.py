# -*- coding: utf-8 -*-


## TrackerPrefix - keeps track of param group prefixes
class TrackerPrefix(object):

        ''' Maps groups of params to custom prefixes. '''

        AMPUSH = 'a'
        CUSTOM = 'c'
        INTERNAL = 'i'


## TrackerProtocol - keeps track of param mappings
class TrackerProtocol(object):

        ''' Maps params to named keys. '''

        # Internal Params
        DEBUG = "d"
        DRYRUN = "n"
        SENTINEL = "x"

        # Basic Event Params
        REF = "r"
        TYPE = "t"
        CONTRACT = "c"
        SPEND = "s"
        PROVIDER = "p"

