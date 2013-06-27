# -*- coding: utf-8 -*-

"""
Protocol: Transport Bindings

Contains static and dynamic bindings for different
transport layers supported by ``Hermes``.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# meta protocol
from . import meta


## HTTPResponseMode
# Enumerates options for how the EventTracker can respond to an event.
class HTTPResponseMode(meta.ProtocolDefinition):

    ''' Enumerates ways a request can be responded to. '''

    IMG = 0x0  # indicates we should respond with an empty GIF.
    JAVASCRIPT = 0x1  # indicates we should respond with tracker JS.
    REDIRECT_TEMP = 0x2  # indicates a temporary (302-code) redirect should be used.
    REDIRECT_PERM = 0x3  # indicates a permanent (301-code) redirect should be used.
    BEACON = 0x4  # indicates that an HTTP 204 No-Content beacon should be used.
    EXPLICIT = 0x5  # indicates that content is allowed to be returned in a given situation


## InputChannel
# Maps input channels for `EventTracker`/`Hermes` to discrete values.
class InputChannel(meta.ProtocolDefinition):

    ''' Maps channels of input to discrete values. '''

    RPC = 0x1  # Indicates that a hit is coming in through RPC.
    HTTP = 0x2  # Indicates that a hit is coming in through regular HTTP.
    INTERNAL = 0x3  # Indicates that a hit is coming in through the Python API directly.
    JAVASCRIPT = 0x4  # Indicates that a hit is coming in through the JS tracking client.


## TransportConfig
# Configures settings for a specific transport for a specific profile.
class TransportConfig(meta.ProtocolBinding):

    ''' General settings to be applied to a specific
        transport for a specific profile. '''

    transport = InputChannel.INTERNAL


## HTTPTransportConfig
# Configures settings for HTTP-specific functionality.
class HTTPTransportConfig(TransportConfig):

    ''' Configures HTTP functionality. '''

    transport = InputChannel.HTTP
    response_mode = HTTPResponseMode.BEACON
