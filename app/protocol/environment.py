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


## BrowserEnvironment
# Defines and enumerates browser environment property names.
class BrowserEnvironment(meta.ProtocolDefinition):

    ''' Defines and enumerates browser environment property
        names. '''

    OS = 'bo'  # browser underlying OS (i.e. 'Mac OS X')
    ARCH = 'bh'  # browser OS architecture (i.e. 'x86_64')
    VENDOR = 'bv'  # browser vendor (i.e. 'Google' or 'Mozilla')
    BROWSER = 'br'  # browser product name (i.e. 'Chrome' or 'Firefox')
