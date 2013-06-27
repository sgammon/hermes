# -*- coding: utf-8 -*-

"""
Protocol: Response Bindings

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# meta protocol
from . import meta


## ResponseMode
# Enumerates options for how the EventTracker can respond to an event.
class ResponseMode(meta.ProtocolDefinition):

    ''' Enumerates ways a request can be responded to. '''

    IMG = 0x0  # indicates we should respond with an empty GIF.
    JAVASCRIPT = 0x1  # indicates we should respond with tracker JS.
    REDIRECT_TEMP = 0x2  # indicates a temporary (302-code) redirect should be used.
    REDIRECT_PERM = 0x3  # indicates a permanent (301-code) redirect should be used.
    BEACON = 0x4  # indicates that an HTTP 204 No-Content beacon should be used.
