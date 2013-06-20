# -*- coding: utf-8 -*-

from protocol.parameter.group import ParamDeclarationMode


# ParameterGroup decorators


def declaration(group):

    ''' Mark a parameter group declaration as a
        "binding block", indicating a set of
        schema-mapped structure items instead
        of values.

        :param group:
        :returns: '''

    ## mark group as a binding block
    group.__mode__ = ParamDeclarationMode.DECLARATION
    return group


def override(group):

    ''' Mark a parameter group declaration as a
        "override block", indicating that it
        should replace blocks of the same name
        _completely_.

        :param group:
        :returns: '''

    ## mark group as an override block
    group.__mode__ = ParamDeclarationMode.OVERRIDE
    return group


def differential(group):

    ''' Coming soon.

        :param group:
        :returns: '''

    ## mark group as a binding block
    group.__mode__ = ParamDeclarationMode.DIFFERENTIAL
    return group


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


# Parameter decorators

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
