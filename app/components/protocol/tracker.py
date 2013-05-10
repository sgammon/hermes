# -*- coding: utf-8 -*-

'''

Components: Tracker Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# Protocol
from . import meta

# protocol components
from components.protocol import event
from components.protocol import param


## TrackerMode - keeps track of modes the tracker can run in
class TrackerMode(meta.ProtocolDefinition):

    ''' Maps tracker modes to discrete values. '''

    DEBUG = 'debug'
    DRYRUN = 'dryrun'
    PRODUCTION = 'production'


## TrackerPrefix - keeps track of param group prefixes
class TrackerPrefix(meta.ProtocolDefinition):

    ''' Maps groups of params to custom prefixes. '''

    AMPUSH = 'a'
    CUSTOM = 'c'
    INTERNAL = 'i'


## TrackerProtocol - keeps track of param mappings
class TrackerProtocol(meta.ProtocolDefinition):

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


## BuiltinParameters
# Describes builtin parameter names.
class BuiltinParameters(meta.ProtocolDefinition):

    ''' Binds names to builtin parameters. '''

    TYPE = 'et'
    PROVIDER = 'pr'
    REF = 'ref'
    SENTINEL = 'x'
    CONTRACT = 'c'
    DEBUG = 'd'
    DRYRUN = 'dry'
    FLUSH = 'flush'


## BuiltinParameterConfig - keeps track of types and defaults for top-level params
class BuiltinParameterConfig(meta.ProtocolDefinition):

    ''' Maps params to types and defaults. '''

    ## Format: <type>, {options}

    ## Types:
    ##   -- builtin basetypes (bool/int/float/basestring)
    ##   -- datetime objects (datetime/time/date)
    ##   -- another ProtocolDefinition class

    ## Options:
    ##   -- policy: ParamPolicy.[ENFORCED|REQUIRED|PREFERRED|OPTIONAL]
    ##   -- default: <default_value>

    TYPE = event.EventType, {'policy': param.ParameterPolicy.REQUIRED}
    PROVIDER = event.EventProvider, {'policy': param.ParameterPolicy.REQUIRED}
    REF = param.ParameterBasetype.STRING, {'policy': param.ParameterPolicy.PREFERRED}
    SENTINEL = param.ParameterBasetype.STRING, {'policy': param.ParameterPolicy.ENFORCED}
    CONTRACT = param.ParameterBasetype.STRING, {'policy': param.ParameterPolicy.PREFERRED}
    DEBUG = param.ParameterBasetype.BOOLEAN, {'default': False, 'policy': param.ParameterPolicy.OPTIONAL}
    DRYRUN = param.ParameterBasetype.BOOLEAN, {'default': False, 'policy': param.ParameterPolicy.OPTIONAL}
