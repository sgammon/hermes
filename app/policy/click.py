# -*- coding: utf-8 -*-

'''

Policy: Clicks

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# event profiles
from .base import http, event, builtin, parameter, transport, decorators, EventProfile


## Click
# Default profile for a ``Click``.
class Click(EventProfile):

    ''' Event Profile describing the basic case for a
        **click**. '''

    class BaseHTTPConfig(transport.HTTPTransportConfig):

        ''' Specifies transport settings for the builtin
            HTTP transport context. '''

        response_mode = transport.HTTPResponseMode.REDIRECT_TEMP

    @decorators.values
    class Base(parameter.ParameterGroup):

        ''' Parameter group for base tracker parameters. '''

        # Type: should be set to `CLICK` for this and descendents.
        type = event.EventType.CLICK

    @decorators.declaration
    class Destination(parameter.ParameterGroup):

        ''' Details and config for this click's redirect. '''

        params = dict
        redirect = bool, {'default': True}

        url = basestring, {
            'source': (http.DataSlot.PARAM, http.DataSlot.HEADER),
            'name': (builtin.TrackerProtocol.DESTINATION, 'destination')
        }
