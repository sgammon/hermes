# -*- coding: utf-8 -*-

"""
Protocol: Attribution

Defines protocol binding classes that build attributed
data for ``Hermes`` events.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# meta protocol
from protocol import meta


## Attribution
# Defines a linked :py:class:`Attribution` spec.
class Attribution(meta.ProtocolBinding):

    def __init__(self, *args, **kwargs):

        ''' Initialize this ``Attribution``. '''

        print "Attribution(%s, %s)" % (args, kwargs)
