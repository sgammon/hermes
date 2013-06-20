# -*- coding: utf -8 -*-

'''
Policy: Illuminite Run
'''

# base clients
from policy import base

# protocol imports
from protocol import http
from protocol import parameter


## IlluminiteRun
# Legacy event policy for trackers owned by Illuminite Run.
class IlluminiteRun(base.LegacyPolicy):

    ''' Legacy policy for events owned by Illuminite Run. '''

    refcode = 'illuminite'

    class Event(parameter.ParameterGroup):

        event_name = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'name': 'event',
            'source': http.DataSlot.PARAM
        }
