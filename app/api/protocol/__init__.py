# -*- coding: utf-8 -*-

"""
Components: Protocol

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

__doc__ = "Protocol definition suite for Ampush Tracker API."
__version__ = (0, 5)

# Top-level protocol extensions
from . import meta

# Meta Bindings
from .meta import Definition
from .meta import ProtocolDefinition

__extensions__ = [meta]

__bindings__ = [
    Definition,
    ProtocolDefinition
]

__all__ = __extensions__ + __bindings__
