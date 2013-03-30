# -*- coding: utf-8 -*-


## TrackerMode - keeps track of modes the tracker can run in
class TrackerMode(object):

        ''' Maps tracker modes to discrete values. '''

        DEBUG = 'debug'
        DRYRUN = 'dryrun'
        PRODUCTION = 'production'


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