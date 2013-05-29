# -*- coding: utf-8 -*-

from protocol.parameter.group import ParamDeclarationMode

# Parameter decorators


def declaration(group):

    ''' Mark a parameter group declaration as a
        "binding block", indicating a set of
        schema-mapped structure items instead
        of values.

        :param group:
        :returns: '''

    ## mark group as a binding block
    group.__mode__ = ParamDeclarationMode.DECLARATION


def override(group):

    ''' Mark a parameter group declaration as a
        "override block", indicating that it
        should replace blocks of the same name
        _completely_.

        :param group:
        :returns: '''

    ## mark group as an override block
    group.__mode__ = ParamDeclarationMode.OVERRIDE


def values(group):

    ''' Mark a parameter group declaration as a
        "values block", indicating a set of
        mapped default values instead of
        ``tuple(basetype, options)``.

        :param group:
        :returns: '''

    ## mark group as a values block
    group.__mode__ = ParamDeclarationMode.VALUES
    return group
