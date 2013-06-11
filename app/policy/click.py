# -*- coding: utf-8 -*-

'''

Policy: Clicks

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# event profiles
from policy.base import EventProfile

# protocol suite
from protocol import http
from protocol import event
from protocol import builtin
from protocol import parameter
from protocol import transport
from protocol.decorators import param
from protocol.parameter.group import ParameterGroup


## Click
# Default profile for a ``Click``.
class Click(EventProfile):

    ''' Event Profile describing the basic case for a
        **click**. '''

    class BaseHTTPConfig(transport.HTTPTransportConfig):

        ''' Specifies transport settings for the builtin
            HTTP transport context. '''

        response_mode = transport.HTTPResponseMode.REDIRECT_TEMP

    @param.values
    class Base(ParameterGroup):

        ''' Parameter group for base tracker parameters. '''

        # Type: should be set to `CLICK` for this and descendents.
        type = event.EventType.CLICK

    @param.declaration
    class Destination(ParameterGroup):

        ''' Details and config for this click's redirect. '''

        url = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'source': (http.DataSlot.PARAM, http.DataSlot.HEADER),
            'name': (builtin.TrackerProtocol.DESTINATION, 'Destination')
        }

        params = dict, {}
        redirect = bool, {'default': True}
