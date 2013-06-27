# -*- coding: utf-8 -*-

'''

Policy: Conversions

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# event profiles
from .base import event, transport, parameter, decorators, EventProfile


## Conversion
# Default profile for a ``Conversion``.
class Conversion(EventProfile):

    ''' Event Profile describing the basic case for a
        **conversion**. '''

    class BaseHTTPConfig(transport.HTTPTransportConfig):

        ''' Specifies transport settings for the builtin
            HTTP transport context. '''

        response_mode = transport.HTTPResponseMode.IMG

    @decorators.values
    class Base(parameter.ParameterGroup):

        ''' Parameter group for base tracker parameters. '''

        type = event.EventType.CONVERSION
