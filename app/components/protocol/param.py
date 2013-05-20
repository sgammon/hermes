# -*- coding: utf-8 -*-

'''
Components: Parameter Protocol

Description coming soon.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Protocol
from . import meta
from .event import EventType, EventProvider


## ParameterBasetype - maps basetypes available for parameters.
class ParameterBasetype(meta.ProtocolDefinition):

    ''' Binds available parameter bastypes to type classes and IDs. '''

    ## == Builtin Basetypes == ##  (can be extended to introduce new types)
    FLOAT = float  # floating-point type
    INTEGER = int  # integer type
    STRING = basestring  # string-type (default, usually)
    BOOLEAN = bool  # boolean type (under HTTP: accepts 'on'/'off', '1'/'0', 'true'/'false' and is case-insensitive)


## ParameterPolicy - specifies ways the presence of an individual param may be handled.
class ParameterPolicy(meta.ProtocolDefinition):

    ''' Maps policy options for a parameter to named items. '''

    ## == Policy Options == #  (in descending order of severity)
    ENFORCED = 0  # refuse requests that are missing this parameter with a 400-range error
    REQUIRED = 1  # accept requests, but mark them as errors if they are missing this parameter
    PREFERRED = 2  # it is valid not to include it, but doing so boosts this request's priority in the buffer
    OPTIONAL = 3  # this parameter is completely optional and has no effect on execution decision making
