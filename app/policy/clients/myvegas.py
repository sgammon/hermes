# -*- coding: utf -8 -*-

'''
Policy: myVEGAS
'''

# base clients
from policy import base

# protocol imports
from protocol import http
from protocol import parameter


## MyVegas
# Legacy event profile for trackers owned by MyVegas.
class MyVegas(base.LegacyProfile):

    ''' Legacy event profile for trackers owned by MyVegas. '''

    refcode = 'myvegas'

    class Event(parameter.ParameterGroup):

        event_name = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'event',
            'source': http.DataSlot.PARAM
        }
