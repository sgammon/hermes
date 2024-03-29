# -*- coding: utf-8 -*-

"""
Hermes: Protocol

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

__doc__ = "Protocol definition suite for Ampush Hermes."
__version__ = (0, 5)


# Top-level protocol extensions
from . import meta
from . import http
from . import event
from . import builtin
from . import special
from . import timedelta
from . import transport
from . import environment

# Sub-protocol extensions
from . import parameter
from . import decorators
from . import attribution
from . import aggregation
from . import integration

__extensions__ = __all__ = [
    'meta', 'http', 'event',
    'builtin', 'special', 'transport',
    'timedelta', 'parameter', 'decorators',
    'environment', 'decorators', 'attribution',
    'aggregation', 'integration'
]
