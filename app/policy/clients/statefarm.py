# -*- coding: utf -8 -*-

'''
Policy: State Farm
'''

# policy imports
from policy import base
from policy import conversion

# protocol imports
from protocol import meta
from protocol import http
from protocol import parameter
from protocol import timedelta
from protocol import aggregation
from protocol.decorators import param


class InsuranceTypes(meta.ProtocolDefinition):

    ''' Lists insurance types that StateFarm provides. '''

    BOAT = 0x1  # boat insurance
    HOUSE = 0x2  # house insurance
    CAR = 0x3  # car insurance
    LIFE = 0x4  # life insurance


class StateFarmConversionLevels(meta.ProtocolDefinition):

    ''' Map State Farm conversion levels to integers. '''

    ONE = 0x1
    TWO = 0x2
    THREE = 0x3


class StateFarm(base.EventProfile):

    ''' Models StateFarm stuff. '''

    refcode = 'statefarm'

    @param.values
    class Base(parameter.ParameterGroup):

        ''' Override contract to always be ``statefarm``. '''

        contract = 'statefarm'

    @param.differential
    class Base(parameter.ParameterGroup):

        ''' Override ``contract`` to look at ``REF``. '''

        contract = basestring, {
            'name': 'ref'
        }

    @param.override
    class Funnel(parameter.ParameterGroup):

        ''' Override adgroup name to ``asid``. '''

        ref = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'source': http.DataSlot.PARAM,
            'name': 'ref'
        }

        adgroup = basestring, {
            'policy': parameter.ParameterPolicy.REQUIRED,
            'source': http.DataSlot.PARAM,
            'name': 'asid'
        }


class StateFarmConversion(StateFarm, conversion.Conversion):

    ''' Details for StateFarm conversions. '''

    class ConversionInfo(parameter.ParameterGroup):

        ''' Describe extra information about a ``StateFarm`` conversion. '''

        level = int, {
            'policy': parameter.ParameterPolicy.PREFERRED,
            'source': http.DataSlot.PARAM,
            'name': 'conv',
            'binding': StateFarmConversionLevels,
            'default': StateFarmConversionLevels.ONE
        }
