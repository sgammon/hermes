# -*- coding: utf-8 -*-

#
#  DOCS COMING SOON! :)
#

__doc__ = "Protocol definition suite for Ampush Tracker API."
__version_ = (0, 1)

# Top-level protocol extensions
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
from .tracker import TrackerPrefix
from .tracker import TrackerProtocol

__extensions__ = [http, event, param, tracker]
__bindings__ = [ResponseStage, EventType, EventProvider, ParamConfig, TrackerPrefix, TrackerProtocol]

