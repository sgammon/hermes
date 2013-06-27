# -*- coding: utf-8 -*-

"""
Protocol: Parameter Decorators

Defines utility decorators that aid in the definition
and creation of :py:class:`ParameterGroup` objects,
which encapsulate :py:class:`Parameter` objects and are
linked to :py:class:`Profile` classes.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# Group Bindings
from protocol.parameter import group as bindings


def declaration(group):

    ''' Mark a parameter group declaration as a
        "binding block", indicating a set of
        schema-mapped structure items instead
        of values.

        :param group: :py:class:`ParameterGroup` to be
        decorated as a ``declaration`` group.

        :returns: Decorated :py:class:`ParameterGroup`. '''

    ## mark group as a binding block
    group.__mode__ = bindings.ParamDeclarationMode.DECLARATION
    return group


def override(group):

    ''' Mark a parameter group declaration as a
        "override block", indicating that it
        should replace blocks of the same name
        _completely_.

        :param group: :py:class:`ParameterGroup` to be
        decorated as an ``override`` group.

        :returns: Decorated :py:class:`ParameterGroup`. '''

    ## mark group as an override block
    group.__mode__ = bindings.ParamDeclarationMode.OVERRIDE
    return group


def differential(group):

    ''' Mark a parameter group declaration as a
        "differential block", indicating that it
        should merge configuration and default
        values with any parent :py:class:`ParameterGroup`
        objects by the same name.

        :param group: :py:class:`ParameterGroup` to be
        decorated as a ``differential`` group.

        :returns: Decorated :py:class:`ParameterGroup`. '''

    ## mark group as a binding block
    group.__mode__ = bindings.ParamDeclarationMode.DIFFERENTIAL
    return group


def values(group):

    ''' Mark a parameter group declaration as a
        "values block", indicating a set of
        mapped default values instead of
        ``tuple(basetype, options)``.

        :param group: :py:class:`ParameterGroup` to be
        decorated as a ``values`` group.

        :returns: Decorated :py:class:`ParameterGroup`. '''

    ## mark group as a values block
    group.__mode__ = bindings.ParamDeclarationMode.VALUES
    return group
