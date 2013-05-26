# -*- coding: utf-8 -*-

'''

Components: Tracker Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# Protocol
from . import meta
from . import event
from . import param

# models
from api.models.tracker import endpoint


## TrackerMode - keeps track of modes the tracker can run in
class TrackerMode(meta.ProtocolDefinition):

    ''' Maps tracker modes to discrete values. '''

    DEBUG = 'debug'
    DRYRUN = 'dryrun'
    PRODUCTION = 'production'


## TrackerProtocol - keeps track of param mappings
class TrackerProtocol(meta.ProtocolDefinition):

    ''' Maps params to named keys. '''

    # Internal Params
    DEBUG = 'd'
    DRYRUN = 'n'
    SENTINEL = 'x'

    # Basic Event Params
    REF = 'r'
    TYPE = 't'
    TRACKER = 'id'
    CONTRACT = 'c'
    SPEND = 's'
    PROVIDER = 'p'


## BuiltinParameters - keeps track of types and defaults for top-level params
#class BuiltinParameters(meta.ProtocolBinding):
#
#    ''' Maps params to types and defaults. '''
#
#    ## Format: <type>, {options}
#
#    ## Types:
#    ##   -- builtin basetypes (bool/int/float/basestring)
#    ##   -- datetime objects (datetime/time/date)
#    ##   -- another ProtocolDefinition class
#
#    ## Options:
#    ##   -- policy: ParamPolicy.[ENFORCED|REQUIRED|PREFERRED|OPTIONAL]
#    ##   -- default: <default_value>
#
#    TYPE = event.EventType, {'policy': param.ParameterPolicy.REQUIRED}
#    TRACKER = endpoint.Tracker, {'policy': param.ParameterPolicy.REQUIRED}
#    PROVIDER = event.EventProvider, {'policy': param.ParameterPolicy.REQUIRED}
#    REF = param.ParameterBasetype.STRING, {'policy': param.ParameterPolicy.PREFERRED}
#    SENTINEL = param.ParameterBasetype.STRING, {'policy': param.ParameterPolicy.ENFORCED}
#    CONTRACT = param.ParameterBasetype.STRING, {'policy': param.ParameterPolicy.PREFERRED}
#    DEBUG = param.ParameterBasetype.BOOLEAN, {'default': False, 'policy': param.ParameterPolicy.OPTIONAL}
#    DRYRUN = param.ParameterBasetype.BOOLEAN, {'default': False, 'policy': param.ParameterPolicy.OPTIONAL}
