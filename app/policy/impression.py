# -*- coding: utf-8 -*-

'''

Policy: Impressions

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# event profiles
from policy.base import EventProfile

# protocol suite
from protocol import event
from protocol.decorators import param
from protocol.parameter.group import ParameterGroup


## Impression
# Default profile for an ``Impression``.
class Impression(EventProfile):

    ''' Event Profile describing the basic case for an
        *Profile*. '''

    @param.values
    class Base(ParameterGroup):

        ''' Parameter group for base tracker parameters. '''

        type = event.EventType.IMPRESSION
