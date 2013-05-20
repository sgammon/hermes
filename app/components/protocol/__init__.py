# -*- coding: utf-8 -*-

'''
Components: Protocol

Description coming soon.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

__doc__ = "Protocol definition suite for Ampush Tracker API."
__version__ = (0, 2)

# Top-level protocol extensions
from . import meta
from . import http
from . import event
from . import param
from . import tracker

# Meta Bindings
from .meta import Definition
from .meta import ProtocolDefinition

# HTTP Bindings
from .http import RequestMethod
from .http import ResponseStage

# Event Bindings
from .event import EventType
from .event import EventProvider
from .event import EventProperty
from .event import EventTypePriority

# Param Bindings
from .param import ParameterPolicy
from .param import ParameterBasetype

# Tracker Bindings
from .tracker import TrackerMode
from .tracker import TrackerPrefix
from .tracker import TrackerProtocol
from .tracker import BuiltinParameters


__extensions__ = [http, event, param, tracker]

__bindings__ = [
    Definition,
    ProtocolDefinition,
    RequestMethod,
    ResponseStage,
    EventType,
    EventProvider,
    EventProperty,
    EventTypePriority,
    ParameterPolicy,
    ParameterBasetype,
    TrackerMode,
    TrackerPrefix,
    TrackerProtocol,
    BuiltinParameters
]

__all__ = __extensions__ + __bindings__
