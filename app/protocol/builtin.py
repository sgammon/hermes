# -*- coding: utf-8 -*-

'''

Components: Tracker Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# Protocol
from . import meta


## TrackerMode - keeps track of modes the tracker can run in
class TrackerMode(meta.ProtocolDefinition):

    ''' Maps tracker modes to discrete values. '''

    ## == Tracker Modes == #
    DEBUG = 'debug'  # debug: puts the tracker in debug mode, which enables logging and halts on exception.
    DRYRUN = 'dryrun'  # dryrun: puts the tracker in ``dryrun`` mode, which disables write commits.
    PRODUCTION = 'production'  # production: puts the tracker in ``production`` mode, which squelches non-data logs unless a problem occurs.


## TrackerHeaders - keeps track of request header mappings.
class TrackerHeaders(meta.ProtocolDefinition):

    ''' Maps tracker control headers to names. '''

    RESPONSE_MODE = 'XET-Mode'


## TrackerProtocol - keeps track of param mappings
class TrackerProtocol(meta.ProtocolDefinition):
    ''' Maps params to named keys. '''

    # == Internal Params == #
    DEBUG = 'd'  # param name for debug mode
    DRYRUN = 'n'  # param name for dryrun mode
    SENTINEL = 'x'  # param name for sentinel

    # Basic Event Params
    TYPE = 't'  # event type code or string
    TRACKER = 'id'  # tracker id
    PROVIDER = 'p'  # event provider

    # Ad-based Params
    ADGROUP = 'g'  # ad group reference
    CAMPAIGN = 'cc'  # ad campaign reference
    CONTRACT = 'ct'  # contract / scope reference
    SPEND = 's'  # total spend amount

    # Builtin click params
    DESTINATION = 'u'  # destination for click redirect
