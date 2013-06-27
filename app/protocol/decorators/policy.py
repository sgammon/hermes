# -*- coding: utf-8 -*-

"""
Protocol: Policy Decorators

Defines utility decorators that aid in top-level
construction of :py:class:`Profile` classes.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""


def legacy(ref=None):

    ''' Wrap a :py:class:`Profile` definition with
        injected config that decribes it as supporting
        ``legacy``-type events. Chief among this is
        adding a `refcode` value to resolve the
        correct :py:class:`Profile` at runtime.

        :param ref: Target ``refcode`` value for defined
        :py:class:`Profile`. Can be ``str``/``unicode``
        for single-ref profiles, and ``frozenset``/``set``
        or ``list/tuple`` for multi-ref profiles, where
        each value is of type ``str`` or ``unicode``.

        :returns: Decorated :py:class:`Profile`, with
        activated support for legacy tracking. '''

    if ref is None:
        raise ValueError('Must provide `ref` to enable target `Profile` for legacy tracking.')

    def decorate(klass):

        ''' Decorate the target class with the encapsulated
            ``ref`` value. '''

        if isinstance(ref, basestring):
            klass.refcode = ref.lower().strip()

        elif isinstance(ref, (frozenset, set, list, tuple)):
            _multiref = []
            for i in ref:
                if not isinstance(i, basestring):
                    raise TypeError('Cannot provide non-string `ref` for legacy tracking'
                                    'profile %s. Got: "%s".' % (str(klass), str(i)))

                _multiref.append(i.lower().strip())
            klass.refcode = frozenset(_multiref)
        return klass
    return decorate  # return internal closure
