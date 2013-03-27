# -*- coding: utf-8 -*-
from .event import EventType, EventProvider


## ParamConfig - keeps track of types and defaults for params
class ParamConfig(object):

        ''' Maps params to types and defaults. '''

        ## Format: <default_value>, <type>

        DEBUG = False, bool
        DRYRUN = False, bool
        REF = None, basestring
        TYPE = EventType.IMPRESSION, basestring
        CONTRACT = None, basestring
        SPEND = None, float(0)
        PROVIDER = EventProvider.FACEBOOK, basestring

