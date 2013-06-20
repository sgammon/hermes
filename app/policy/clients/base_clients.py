# -*- coding: utf -8 -*-

'''
Policy: Base Clients
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


class BaseClients(base.EventProfile):

    class Legacy(parameter.ParameterGroup):

        ref = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'ref',
            'source': http.DataSlot.PARAM
        }

        adid = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': ('adid', 'asid', 'ad_id'),
            'source': http.DataSlot.PARAM
        }

    class ConversionLevel(parameter.ParameterGroup):

        conversion = bool, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'conv',
            'source': http.DataSlot.PARAM
        }

        conversion2 = bool, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'conv2',
            'source': http.DataSlot.PARAM
        }

        conversion3 = bool, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'conv3',
            'source': http.DataSlot.PARAM
        }

        conversion4 = bool, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'conv4',
            'source': http.DataSlot.PARAM
        }

        conversion5 = bool, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'conv5',
            'source': http.DataSlot.PARAM
        }

        conversion6 = bool, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'conv6',
            'source': http.DataSlot.PARAM
        }

        conversion7 = bool, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'conv7',
            'source': http.DataSlot.PARAM
        }

        conversion8 = bool, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'conv8',
            'source': http.DataSlot.PARAM
        }

        conversion9 = bool, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'conv9',
            'source': http.DataSlot.PARAM
        }

        conversion10 = bool, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'conv10',
            'source': http.DataSlot.PARAM
        }
