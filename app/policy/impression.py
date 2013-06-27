# -*- coding: utf-8 -*-

'''

Policy: Impressions

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# event profiles
from .base import event, transport, parameter, decorators, EventProfile


## Impression
# Default profile for an ``Impression``.
class Impression(EventProfile):

    ''' Event Profile describing the basic case for an
        *Profile*. '''

    class BaseHTTPConfig(transport.HTTPTransportConfig):

        ''' Specifies transport settings for the builtin
            HTTP transport context. '''

        response_mode = transport.HTTPResponseMode.IMG

    @decorators.values
    class Base(parameter.ParameterGroup):

        ''' Parameter group for base tracker parameters. '''

        type = event.EventType.IMPRESSION
