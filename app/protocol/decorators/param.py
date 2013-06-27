# -*- coding: utf-8 -*-

"""
Protocol: Parameter Decorators

Defines utility decorators that aid in the definition
and creation of :py:class:`Parameter` objects being
linked to :py:class:`Profile` classes.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""


def parameter(basetype=basestring, config=None, **kwconfig):

    ''' Wrap a callable and make it a parameter,
        assigning any config passed-in and attaching
        the decorated callable as the constructed
        :py:class:`Parameter` mapper.

        :param basetype: Type constructor for the
        target parameter. Defaults to ``basestring``,
        which is fine for most applications.

        :param config: Positional ``dict`` config to
        pass in to constructed :py:class:`Parameter`.

        :param **config: Kwarg-style ``dict`` config
        to pass in to constructed :py:class:`Parameter`.
        Overrides entries in positional ``config``.

        :returns: Factoried parameter spec - ``basetype``,
        ``config`` tuple for use in :py:class:`Profile`
        descendants. '''

    # resolve and merge config
    if not config: config = {}
    config.update(kwconfig)

    def wrap_parameter(mapper_fn):

        ''' Nested closure wrapper for decorating
            inline :py:class:`Parameter` mappers.

            :param callable: Mapper to be decorated.

            :returns: Wrapped mapper and generated
            :py:class:`Parameter` spec. '''

        config['mapper'] = mapper_fn
        return basetype, config

    return wrap_parameter
