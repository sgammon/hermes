# -*- coding: utf-8 -*-

"""
Protocol: Decorators

Defines utility decorators that aid in the construction
of bound :py:class:`Profile` classes.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# decorator groups
from . import param
from . import group
from . import policy

# policy decorators
from .policy import legacy

# param / group decorators
from .param import parameter
from .group import declaration, override, differential, values


__all__ = ['param',
           'group',
           'policy',
           'legacy',
           'parameter',
           'declaration',
           'override',
           'differential',
           'values']
