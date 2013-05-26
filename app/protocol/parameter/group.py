# -*- coding: utf-8 -*-

'''

Parameter Protocol: Group

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# Protocol
from protocol import meta


# ParamDeclarationMode - enumerates possible mode options for a ``ParameterGroup``.
class ParamDeclarationMode(meta.ProtocolDefinition):

    ''' Specifies the declaration mode for a
        :py:class:`ParameterGroup` block. '''

    DECLARATION = 0x1  # ``declaration`` state (default) - indicates a ``ParameterGroup`` is declaring parameters.
    VALUES = 0x2  # ``values`` state - indicates a ``ParameterGroup`` is filling in default or static values.
    OVERRIDE = 0x3  # ``override`` state - indicates a full (non-delta) property override state.


## ParameterGroup - utility/encapsulation class for extending and defining a parameter group's specs.
class ParameterGroup(meta.ProtocolBinding):

    ''' Abstract base for a group of params. '''

    __mode__ = ParamDeclarationMode.DECLARATION  # default mode - ``declaration``
