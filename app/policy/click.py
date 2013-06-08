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
from protocol import intake
from protocol import builtin
from protocol import response
from protocol import parameter
from protocol.decorators import param
from protocol.parameter.group import ParameterGroup


## Click
# Default profile for a ``Click``.
class Click(EventProfile):

    ''' Event Profile describing the basic case for a
        **click**. '''

    @param.values
    class Base(ParameterGroup):

        ''' Parameter group for base tracker parameters. '''

        # Type: should be set to `CLICK` for this and descendents.
        type = event.EventType.CLICK

        # Mode: should almost always be set to a `REDIRECT` type for `CLICK`.
        mode = response.ResponseMode.REDIRECT_TEMP

    @param.values
    class System(ParameterGroup):

        ''' Indicate the input channel for 'CLICK'. '''

        # Channel: clicks usually come in through HTTP.
        channel = intake.InputChannel.HTTP

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
