# -*- coding: utf-8 -*-

# Parameter decorators


def values(group):

    ''' Mark a parameter group declaration as a
        "values block", indicating a set of
        mapped default values instead of
        ``tuple(basetype, options)``.

        :param group:
        :returns: '''

    return group
