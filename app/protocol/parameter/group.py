# -*- coding: utf-8 -*-

"""
Parameter Protocol: Group Bindings

Defines and structures bindings for creating parameter
groups.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# meta protocol
from .. import meta


# ParamDeclarationMode
# Enumerates possible mode options for a ``ParameterGroup``.
class ParamDeclarationMode(meta.ProtocolDefinition):

    ''' Specifies the declaration mode for a
        :py:class:`ParameterGroup` block. '''

    DECLARATION = 0x1  # ``declaration`` state (default) - indicates a ``ParameterGroup`` is declaring parameters.
    VALUES = 0x2  # ``values`` state - indicates a ``ParameterGroup`` is filling in default or static values.
    OVERRIDE = 0x3  # ``override`` state - indicates a full (non-delta) property override state.
    DIFFERENTIAL = 0x4  # ``differential`` state - indicates a delta property override state (``override`` for schema)


## Parameter
# Specifies an individual parameter. Always part of a ``ParameterGroup``.
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
    name = None  # external property name of the :py:class:`Parameter`
    group = None  # reference to the encapsulating/owning :py:class:`ParameterGroup`
    mapper = None  # mapper function defined to handle the property, if any
    policy = None  # reference to the encapsulating/owning :py:class:`Policy`
    parent = None  # reference to immediate parent/inherited :py:class:`Parameter` (if any)
    config = None  # ``dict`` of arbitrary config items that the :py:class:`Interpreter` should understand
    literal = False  # flag indicating that this parameter was defined with a literal call to :py:class:`Parameter`
    basetype = None  # base type constructor to validate and convert values of this :py:class:`Parameter`
    basevalue = None  # base value to use in place of a missing value in a :py:class:`TrackedEvent` (basically default)

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
        if not self.mapper and parent is not None:
            self.mapper = parent.mapper

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

    def _ancestry(self, reverse=False):

        ''' Walk the ancestry tree for this :py:class:`Property`.
            Yields the current property, and then each parent
            property that can be found by recursively walking
            `property.parent`.

            :param reversed: Flag ``bool`` that reverses the
            ancestry order (``root``-> ``n`` -> ``target``),
            instead of the default (``target`` -> ``n`` -> ``root``).
            Defaults to ``False``.

            :returns: A generator that ``yields`` each ancestor. '''

        ancestry = []
        if prop.parent:  # are we at the root?
            parent = prop.parent
            while parent:
                ancestry.append(parent)
                parent = prop.parent

        if reverse:
            for i in reversed(ancestry):
                yield i
            yield self
        else:
            yield self
            for i in ancestry:
                yield i
        raise StopIteration()

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


## ParameterGroup
# Utility/encapsulation class for extending and defining a parameter group's specs.
class ParameterGroup(meta.ProtocolBinding):

    ''' Abstract base for a group of params. '''

    # == Public Members == #
    name = None  # external name of this :py:class:`ParameterGroup`
    parameters = None  # :py:class:`Parameter` objects defined in this group

    # == Internal Members == #
    __mode__ = ParamDeclarationMode.DECLARATION  # default mode - ``declaration``
    __inline__ = None  # ``inline`` flag - whether this was defined with an explicit constructor call

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
