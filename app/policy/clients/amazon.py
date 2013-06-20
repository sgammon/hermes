# -*- coding: utf -8 -*-

'''
Policy: Amazon
'''

# policy imports
from policy import base

# protocol imports
from protocol import http
from protocol import parameter


## Amazon
# Legacy event profile for trackers owned by Amazon.
class Amazon(base.LegacyProfile):

    ''' Base profile for Amazon. '''

    refcode = 'amazon'

    class Order(parameter.ParameterGroup):

        ''' More params. '''

        user_id = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'uid',
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

    class SignatureVerification(parameter.ParameterGroup):

        ''' More params. '''

        signature = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'signature',
            'source': http.DataSlot.PARAM
        }
