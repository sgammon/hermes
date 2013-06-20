# -*- coding: utf -8 -*-

'''
Policy: Blue Apron
'''

# policy imports
from policy import base

# protocol imports
from protocol import http
from protocol import parameter


## BlueApron
# Policy class for trackers owned by Blue Apron.
class BlueApron(base.LegacyProfile):

    ''' Legacy event policy class for trackers owned
        by Blue Apron. '''

    refcode = 'blueapron'

    class Event(parameter.ParameterGroup):

        event_name = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'event',
            'source': http.DataSlot.PARAM
        }
