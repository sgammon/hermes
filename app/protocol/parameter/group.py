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
    DIFFERENTIAL = 0x4  # ``differential`` state - indicates a delta property override state (``override`` for schema)


## Parameter - specifies an individual parameter. Always part of a ``ParameterGroup``.
class Parameter(meta.ProtocolBinding):

    ''' Individual binding for a ``parameter`` on
        an ``EventTracker hit. '''

    ## == Internal Properties == ##
    __slots__ = ('name',
                 'group',
                 'mapper',
                 'policy',
                 'parent',
                 'config',
                 'literal',
                 'basetype',
                 'basevalue')

    ## == External Properties == ##
    name = None
    group = None
    mapper = None
    policy = None
    parent = None
    config = None
    literal = False
    basetype = None
    basevalue = None

    ## == Internal Methods == ##
    def __init__(self, _policy, parent, group, subtype, basetype=None, value=None, **config):

        ''' Initialize this ``Parameter``.

            :param _policy: Eventual ancestor policy class
            (:py:class:`Profile` descendant) that we're
            attaching this :py:class:`ParameterGroup` to.
            Prefixed with underscore to prevent collision
            with ``kwargs``.

            :param parent: Parent property (property of the
            same name defined on a parent policy definition),
            if any.

            :param group: Parameter group name (``str``)
            encapsulating this :py:class:`Parameter`.

            :param subtype: External (bound) name of this
            parameter, on the encapsulating
            :py:class:`EventProfile`.

            :param basetype: Base value type for this
            property.

            :param value: Concrete value, in the case of a
            default or override block.

            :param config: Keyword-argument config ``dict``
            that will be attached to this
            :py:class:`Parameter`.

            :returns: Nothing, as this is a constructor. '''

        # adopt parent param's basetype, if any
        if not basetype and parent is not None:
            basetype = parent.basetype

        # adopt parent param's value, if any
        if not value and parent is not None:
            value = parent.basevalue

        # pluck and attach mapper, if found
        if 'mapper' in config:
            self.mapper = config.get('mapper')
            del config['mapper']

        # attach parent definitions
        self.policy, self.parent = _policy, parent

        # factory parameter
        self.name, self.config, self.basetype, self.basevalue, self.literal = (subtype,
                                                                               config,
                                                                               basetype,
                                                                               value,
                                                                               config.get('literal', False))

    def __repr__(self):

        ''' Generate a string representation for this
            :py:class:`Property` object.

            :returns: Clean string repr. '''

        return "Property(%s, %s)" % (self.name, self.basetype or self.basevalue)

    def set_default(self, default):

        ''' Set this parameter's default value,
            to be used (and stored) in place of
            a full value if none was found.

            :param default: Default value to use
            in place of a full value.

            :returns: ``self``, for chainability. '''

        self.basevalue = default
        return self

    def set_group(self, group):

        ''' Set this parameter's :py:attr:`self.group`.
            Called by the encapsulating group on construction to
            replace the string added during initialization.

            :param group:
            :returns: ``self``, for chainability. '''

        self.group = group
        return self


## ParameterGroup - utility/encapsulation class for extending and defining a parameter group's specs.
class ParameterGroup(meta.ProtocolBinding):

    ''' Abstract base for a group of params. '''

    # == Public Members == #
    name = None
    parameters = None

    # == Internal Members == #
    __mode__ = ParamDeclarationMode.DECLARATION  # default mode - ``declaration``
    __inline__ = None

    def __init__(self, name, spec, inline=False):

        ''' Initialize this :py:class:`ParameterGroup` with
            a set of defined properties.

            :param name: String name of the parameter group
            extension, to be fully-qualified.

            :param spec: Subproperty specification - an
            iterable of :py:class:`Property`
            objects.

            :param inline: Specifies that his group was
            defined inline, rather than attached later.

            :returns: Nothing, as this is a constructor. '''

        self.name, self.parameters, self.__inline__ = name, spec, inline

    def __iter__(self):

        ''' Proxy iteration over this object to yielding
            the grouped :py:class:`Property` objects it
            contains.

            :returns: Yields each encapsulated/owned
            :py:class:`Property`. '''

        for param in self.parameters:
            yield param

    def __len__(self):

        ''' Proxy length checking over this obejct to
            the grouped :py:class:`Property` objects it
            contains.

            :returns: Integer length of an internal list
            containing the defined properties for this
            :py:class:`PropertyGroup`. '''

        return len(self.parameters)
