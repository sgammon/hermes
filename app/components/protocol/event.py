# -*- coding: utf-8 -*-

'''

Components: Event Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# Protocol
from . import meta


## EventType - keeps track of defined event types
class EventType(meta.ProtocolDefinition):

    ''' Keeps track of event types that we track. '''

    CLICK = "c"
    IMPRESSION = "i"
    CONVERSION = "v"


## EventProvider - keeps track of event sources
class EventProvider(meta.ProtocolDefinition):

    ''' Keeps track of sources of events we track. '''

    CLIENT = 'on'
    OFFSITE = 'of'
    AMAZON = 'amz'
    FACEBOOK = 'fb'
    HASOFFERS = 'hs'
