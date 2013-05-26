# -*- coding: utf-8 -*-

'''

Policy: Clicks

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# event profiles
from policy.base import EventProfile

# protocol suite
from protocol import event
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

        type = event.EventType.CLICK