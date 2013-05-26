# -*- coding: utf-8 -*-

'''

Attribution Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# meta protocol
from protocol import meta


## Attribution
#
class Attribution(meta.ProtocolBinding):

    def __init__(self, *args, **kwargs):

        ''' Initialize this ``Attribution``. '''

        print "Attribution(%s, %s)" % (args, kwargs)


## CompoundAttribution
#
class CompoundAttribution(meta.ProtocolBinding):

    def __init__(self, *args, **kwargs):

        ''' Initialize this ``CompoundAttribution``. '''

        print "CompoundAttribution(%s, %s)" % (args, kwargs)
