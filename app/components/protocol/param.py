# -*- coding: utf-8 -*-

'''

Components: Parameter Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# Protocol
from . import meta
from .event import EventType, EventProvider


class ParamPolicy(meta.ProtocolDefinition):

	''' Maps policy options for a parameter to named items. '''

	## Options (in descending order of severity):
	##   -- enforced: refuse requests that are missing this parameter
	##   -- required: accept requests, but mark them as errors if they are missing this parameter
	##   -- preferred: it is valid not to include it, but doing so boosts this request's priority in the buffer
	##   -- optional: this parameter is completely optional and has no effect on execution decision making

	enforced = 0
	required = 1
	preferred = 2
	optional = 3


## ParamConfig - keeps track of types and defaults for top-level params
class ParamConfig(meta.ProtocolDefinition):

    ''' Maps params to types and defaults. '''

    ## Format: <type>, {options}

    ## Types:
    ##   -- builtin basetypes (bool/int/float/basestring)
    ##   -- datetime objects (datetime/time/date)
    ##   -- another ProtocolDefinition class

    ## Options:
    ##   -- policy: ParamPolicy.[enforced|required|preferred|optional]
    ##   -- default: <default_value>

    DEBUG = bool
    DRYRUN = bool
    REF = basestring
    CONTRACT = basestring
    SPEND = float(0)    
    TYPE = EventType, {'default': EventType.IMPRESSION}
    PROVIDER = EventProvider, {'default': EventProvider.FACEBOOK}
