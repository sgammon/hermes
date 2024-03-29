# -*- coding: utf-8 -*-

'''

Policy: Conversions

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# event profiles
from policy.base import EventProfile

# protocol suite
from protocol import event
from protocol import transport
from protocol.decorators import param
from protocol.parameter.group import ParameterGroup


## Conversion
# Default profile for a ``Conversion``.
class Conversion(EventProfile):

    ''' Event Profile describing the basic case for a
        **conversion**. '''

    class BaseHTTPConfig(transport.HTTPTransportConfig):

        ''' Specifies transport settings for the builtin
            HTTP transport context. '''

        response_mode = transport.HTTPResponseMode.IMG

    @param.values
    class Base(ParameterGroup):

        ''' Parameter group for base tracker parameters. '''

        type = event.EventType.CONVERSION
