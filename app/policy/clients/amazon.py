# -*- coding: utf -8 -*-

'''
Policy: Amazon
'''

# policy imports
from policy import base

# protocol imports
from protocol import meta
from protocol import http
from protocol import parameter
from protocol import timedelta
from protocol import aggregation
from protocol.decorators import param


class Amazon(base.EventProfile):

    ''' Base profile for Amazon. '''

    refcode = 'amazon'

    class WhateverName(parameter.ParameterGroup):

        ''' Params or something. '''

        conversion = bool, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'conv',
            'source': http.DataSlot.PARAM
        }

        event_name = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'event',
            'source': http.DataSlot.PARAM
        }

        conversion_type = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'convtype',
            'source': http.DataSlot.PARAM
        }

    class SecondGroupOverHere(parameter.ParameterGroup):

        ''' More params. '''

        ad_id = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'adid',
            'source': http.DataSlot.PARAM
        }

        user_id = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'uid',
            'source': http.DataSlot.PARAM
        }

        signature = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'signature',
            'source': http.DataSlot.PARAM
        }
