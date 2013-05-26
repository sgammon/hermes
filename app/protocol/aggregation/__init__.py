# -*- coding: utf-8 -*-

'''

Aggregation Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# meta protocol
from protocol import meta


## Aggregation
#
class Aggregation(meta.ProtocolBinding):

    def __init__(self, *args, **kwargs):

        ''' Initialize this ``Aggregation``. '''

        print "Aggregation(%s, %s)" % (args, kwargs)
