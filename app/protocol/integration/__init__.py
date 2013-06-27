# -*- coding: utf-8 -*-

"""
Protocol: Integration Bindings

Defines bindings for creating :py:class:`Integration`
objects to be attached to a :py:class:`Profile`,
which fulfill advanced, event-level integration tasks
for internal and external parties.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# meta protocol
from .. import meta


## Integration
# Defines a linked :py:class:`Integration` spec.
class Integration(meta.ProtocolBinding):

    ''' Defines an attached integration to a
        :py:class:`Profile`. '''

    def __init__(self, *args, **kwargs):

        ''' Initialize this ``Integration``. '''

        print "Integration(%s, %s)" % (args, kwargs)
