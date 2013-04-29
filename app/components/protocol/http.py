# -*- coding: utf-8 -*-

'''

Components: HTTP Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# Protocol
from . import meta


## ResponseStage - indicates the status of a request/response cycle
class ResponseStage(meta.ProtocolDefinition):

    ''' Maps request stages to discrete values. '''

    PENDING = 0
    STARTED = 1
    COMPLETE = 2
