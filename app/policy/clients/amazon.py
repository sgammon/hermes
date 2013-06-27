# -*- coding: utf -8 -*-

'''
Policy: Amazon

Event policy suite for Amazon.

:author: Leo Celis (leo.celis@ampush.com)
:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# policy imports
from policy import base
from protocol import parameter, decorators


## Amazon
# Legacy event profile for trackers owned by Amazon.
@decorators.legacy(ref='amazon')
class Amazon(base.LegacyProfile):

    ''' Base profile for Amazon. '''

    @decorators.override
    class Order(parameter.ParameterGroup):

        ''' Encapsulates order details like
            `user_id` and `event_name`. '''

        user_id = basestring, {'name': 'uid'}
        event_name = basestring, {'name': 'event'}
        conversion_type = basestring, {'name': 'convtype'}

    class Signature(parameter.ParameterGroup):

        ''' Parameter group supporting event
            signing and signature verification. '''

        @decorators.parameter(basestring, name='signature')
        def valid(event, data, value):

            ''' Verify event signature present
                in the URL with a configured
                static secret. '''

            return value  # @TODO(sgammon): verify signature
