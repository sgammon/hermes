# -*- coding: utf-8 -*-

from protocol.parameter.group import ParamDeclarationMode

# Parameter decorators


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
