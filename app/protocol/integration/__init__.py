# -*- coding: utf-8 -*-

'''

Integration Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# meta protocol
from protocol import meta


## Integration
#
class Integration(meta.ProtocolBinding):

    def __init__(self, *args, **kwargs):

        ''' Initialize this ``Integration``. '''

        print "Integration(%s, %s)" % (args, kwargs)
