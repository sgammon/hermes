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

    PENDING = 0  # pending - the server is processing the request, no response headers yet
    STARTED = 1  # started - response headers have been sent, waiting to yield content
    COMPLETE = 2  # complete - response has been sent, can no longer yield content
