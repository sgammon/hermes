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

        IMPRESSION = "i"
        CONVERSION = "c"


## EventProvider - keeps track of event sources
class EventProvider(meta.ProtocolDefinition):

        ''' Keeps track of sources of events we track. '''

        FACEBOOK = 'fb'
