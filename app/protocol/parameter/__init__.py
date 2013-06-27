# -*- coding: utf-8 -*-

"""
Protocol: Parameter Bindings

Defines bindings and ancillary structure for creating
defined :py:class:`Parameter` and :py:class:`ParameterGroup`
objects, to be attached to a :py:class:`Policy`.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# Protocol
from .. import meta

# Parameter
from . import group
from .group import Parameter
from .group import ParameterGroup
from .group import ParamDeclarationMode


## ParameterBasetype
# Maps basetypes available for parameters.
class ParameterBasetype(meta.ProtocolDefinition):

    ''' Binds available parameter bastypes to type classes and IDs. '''

    ## == Builtin Basetypes == ##  (can be extended to introduce new types)
    FLOAT = float  # floating-point type
    INTEGER = int  # integer type
    STRING = basestring  # string-type (default, usually)
    BOOLEAN = bool  # boolean type (under HTTP: accepts 'on'/'off', '1'/'0', 'true'/'false' and is case-insensitive)


## ParameterPolicy
# Specifies ways the presence of an individual param may be handled.
class ParameterPolicy(meta.ProtocolDefinition):

    ''' Maps policy options for a parameter to named items. '''

    ## == Policy Options == #  (in descending order of severity)
    ENFORCED = 0x0  # refuse requests that are missing this parameter with a 400-range error
    REQUIRED = 0x1  # accept requests, but mark them as errors if they are missing this parameter
    PREFERRED = 0x2  # it is valid not to include it, but doing so boosts this request's priority in the buffer
    OPTIONAL = 0x3  # this parameter is completely optional and has no effect on execution decision making
    SPECIAL = 0x4  # this parameter is special and has builtin or extended-in code to handle it.


## ParameterType
# Keeps track of param group prefixes
class ParameterType(meta.ProtocolDefinition):

    ''' Maps groups of params to custom prefixes. '''

    ## == Parameter Types == ##
    DATA = 'd'  # indicates that this property holds data that should be stored with the hit.
    AMPUSH = 'a'  # indicates that this is a builtin, ampush-specific property (_not_ system internal, though).
    CUSTOM = 'c'  # indicates a property custom-made for a client or use case, with special code attached
    INTERNAL = 'i'  # indicates a property that is internal to the ``EventTracker`` system


__all__ = ['group', 'Parameter', 'ParameterGroup', 'ParamDeclarationMode']
