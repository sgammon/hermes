# -*- coding: utf-8 -*-

'''

Components: Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

__doc__ = "Protocol definition suite for Ampush Tracker API."
__version__ = (0, 2)

# Top-level protocol extensions
from . import meta
from . import http
from . import event
from . import param
from . import tracker

# HTTP Bindings
from .http import ResponseStage

# Event Bindings
from .event import EventType
from .event import EventProvider

# Param Bindings
from .param import ParamConfig

# Tracker Bindings
from .tracker import TrackerMode
from .tracker import TrackerPrefix
from .tracker import TrackerProtocol


__extensions__ = [http, event, param, tracker]
__bindings__ = [ResponseStage, EventType, EventProvider, ParamConfig, TrackerMode, TrackerPrefix, TrackerProtocol]
