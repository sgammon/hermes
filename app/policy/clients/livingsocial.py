# -*- coding: utf -8 -*-

'''
Policy: LivingSocial

Event policy suite for LivingSocial.

:author: Leo Celis (leo.celis@ampush.com)
:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# policy imports
from policy import base
from protocol import parameter, decorators


## LivingSocial
# Legacy event profile for LivingSocial-owned trackers.
@decorators.legacy(ref=frozenset(['livingsocialUS', 'livingsocialUSstory']))
class LivingSocial(base.LegacyProfile):

    ''' Base profile for LivingSocial. '''

    @decorators.differential
    class Order(parameter.ParameterGroup):

        ''' Custom `Order` group, encapsulating client-specific
            order details like `deal`. '''

        ## Basic params
        user_id = basestring, {'name': 'uid'}
        order = basestring, {'name': 'unique'}
        deal = basestring, {'name': 'deal_id'}

        ## Combined `ref_code`/`ASID`
        @decorators.parameter(basestring, name='ref_code')
        def reference_code(event, data, value):

            ''' Combined `ref_code` and `ASID` parameter. '''

            # make sure we can split
            if '_' not in value:
                raise ValueError('LivingSocial `ref_code` contained to underscore to split by.')

            # attempt to split the `ref_code`
            try:
                refcode, asid = tuple(value.split('_'))  # extract ASID

            except (ValueError, TypeError):
                raise  # re-raise type/value errors

            except Exception as e:
                context = (e.__class__.__name__, str(e))  # re-raise uncaught exceptions as `ValueError`
                raise ValueError('Uncaught exception decoding LivingSocial `refcode`: %s(%s).' % context)

            if refcode and asid:  # properly decoded (set `ASID` and `ref_code`)
                event.refcode = asid
                return refcode

            return refcode  # did not decode (just set `ref_code`)
