# -*- coding: utf-8 -*-

'''

Components: HTTP Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# Protocol
from . import meta


## InputChannel
# Maps input channels for `EventTracker`/`Hermes` to discrete values.
class InputChannel(meta.ProtocolDefinition):

    ''' Maps channels of input to discrete values. '''

    RPC = 0x1  # Indicates that a hit is coming in through RPC.
    HTTP = 0x2  # Indicates that a hit is coming in through regular HTTP.
    INTERNAL = 0x3  # Indicates that a hit is coming in through the Python API directly.
