# -*- coding: utf-8 -*-

'''

Policy Core

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# protocol bindings
from protocol import meta

# protocol extensions
from protocol import parameter
from protocol import integration
from protocol import attribution
from protocol import aggregation

# apptools util
from apptools.util import decorators as util


## Profile
# Metaclass that provides structure for overridable profiles.
class Profile(type):

    ''' Abstract :py:class:`EventProfile` metaclass that provides
        structure for overridable profiles and enforces strict
        schema rules.

        An encapsulated class at :py:attr:`Profile.Interpreter`
        is used to read, merge, and export profile structures
        defined via :py:class:`EventProfile`-subclasses. '''

    registry = {}  # central profile registry

    ## Interpreter
    # Manages interpretation and merging of `Profile` descendents.
    class Interpreter(object):

        ''' Manages interpretation and merging of `Profile`
            descendents, and contains utility functions to
            break each discrete component down into an
            element in a virtual ``AST``-like structure. '''

        ## == Public Members == ##
        primitives = None
        parameters = None
        aggregations = None
        attributions = None
        integrations = None

        ## == Internal Members == ##
        __tree__ = None
        __subtype__ = None
        __profile__ = None
        __compound__ = None
        __interpreted__ = None

        ## == Internals == ##
        def __init__(self, name, specs):

            ''' Instantiate a new ``Interpreter``, and attach
                the given ``profile`` for future work.

                :param profile: :py:class:`EventProfile` subclass
                                to interpret or merge.

                :returns: Nothing, this is a constructor. '''

            self.__subtype__, self.__profile__ = name, specs

        def _build_paramgroup(self, policy, group, klass, inline=True):

            ''' Build a ``ParameterGroup`` object from a direct
                subclass, embedded in a :py:class:`EventProfile`
                definition.

                :param policy: Parent policy class (derivative of
                               :py:class:`EventProfile`) that we
                               are processing for, so we can
                               inform sub-objects.

                :param group: The :py:class:`ParameterGroup`
                              subclass to compile.

                :return: An instantiated and properly filled-out
                        :py:class:`ParameterGroup` object. '''

            # overlay parameter path, init params list
            parameters, mainconfig = [], {
                'definition': {
                    'path': '.'.join(group.__module__.split('.') + [self.__subtype__]),
                    'name': group.__name__
                }
            }

            # build and initialize parameters
            for param, config in dict(((i, group.__dict__[i]) for i in group.__forward__)).iteritems():

                if isinstance(config, tuple):  # we're configuring schema
                    basetype, config = config

                    # update with mainconfig, build and append
                    config.update(mainconfig)
                    current_param = parameter.Parameter(param, basetype, **config)

                else:  # we're probably configuring values

                    value = basetype  # for clarity's sake

                    # use main config, add sentinel for value
                    config = {'mode': parameter.group.ParameterDeclarationMode.VALUES}
                    current_param = parameter.Parameter(param, basetype=None, value=value, **config)

                parameters.append(current_param)

                # consider aggregations
                if config.get('aggregations', None) is not None:

                    # delegate to aggregations
                    for spec in config.get('aggregations'):
                        klass['aggregations'].append(self._build_aggregation(policy, spec, klass, True, current_param))

                # consider attributions
                if config.get('attributions', None) is not None:

                    # delegate to attributions
                    for spec in config.get('attributions'):
                        klass['attributions'].append(self._build_attribution(policy, spec, klass, True, current_param))

            return parameter.ParameterGroup(group.__name__, parameters, inline=inline)

        def _build_integration(self, policy, spec, klass, inline=True):

            ''' Build an ``Integration`` object from a
                specification encountered in a subclass of
                :py:class:`EventProfile`.

                :param policy: Parent policy class (derivative of
                :py:class:`EventProfile`) that we are processing for,
                so we can inform sub-objects.

                :param spec: Class structure and specification, as
                found in the encapsulating :py:class:`EventProfile`.

                :keyword inline: Indicates that this is a subclass
                defined inline in an encapsulating :py:class:`EventProfile`.
                Defaults to ``True``.

                :returns: An instantiated and properly filled-out
                :py:class:`IntegrationGroup` object. '''

            raise NotImplementedError('`Integration` edges are not yet supported by `EventTracker`.')

        def _build_attribution(self, policy, spec, klass, compound=False, owner=None):

            ''' Build an ``Attribution`` or ``CompoundAttribution``
                from a specification encountered in a subclass of
                :py:class:`EventProfile`.


                :param policy: Parent policy class (derivative of
                               :py:class:`EventProfile`) that we
                               are processing for, so we can
                               inform sub-objects.

                :param spec: Class structure and specification, as
                             found in the encapsulating
                             :py:class:`EventProfile`.

                :keyword compound: Indicates that this is a subclass
                                   of :py:class:`CompoundAttribution`,
                                   and may span more than one hashed
                                   property or include special code.
                                   Defaults to ``False``.

                :returns: An instantiated and properly filled-out
                          :py:class:`AttributionGroup` object. '''

            raise NotImplementedError('`Attribution` edges are not yet supported by `EventTracker`.')

        def _build_aggregation(self, policy, spec, klass, compound=False, owner=None):

            ''' Build an ``Aggregation`` or ``CompoundAggregation``
                from a specification encountered in a subclass of
                :py:class:`EventProfile`.

                :param policy: Parent policy class (derivative of
                               :py:class:`EventProfile`) that we
                               are processing for, so we can
                               inform sub-objects.

                :param spec: Class structure and specification, as
                             found in the encapsulating
                             :py:class:`EventProfile`.

                :keyword compound: Indicates that this is a subclass
                                   of :py:class:`CompoundAggregation`,
                                   and may span more than one hashed
                                   property or include special code.
                                   Defaults to ``False``.

                :returns: An instantiated and properly filled-out
                          :py:class:`AggregationGroup` object. '''

            if owner:
                spec.set_owner(owner)
            return spec

        _builders = {
            integration.Integration: ('integrations', _build_integration),
            attribution.Attribution: ('attributions', _build_attribution),
            aggregation.Aggregation: ('aggregations', _build_aggregation),
            parameter.ParameterGroup: ('parameters', _build_paramgroup)
        }

        ## == Public Methods == ##
        def build(self, overlay=None):

            ''' Build a :py:class:`EventProfile` descendent
                into a fully-structured object.

                :returns: ``self``, for method chainability. '''

            # initialize compound structure
            compound = {
                'primitives': [],
                'parameters': [],
                'aggregations': [],
                'attributions': [],
                'integrations': []
            }

            for (parent, subspecs) in self.__profile__.iteritems():
                for spec, spec_klass, flag in subspecs:
                    attr, builder = self._builders[parent]
                    compound[attr].append(builder(self, spec_klass, spec, compound, flag))
                    compound['primitives'].append(spec_klass)

            # assign locally
            for k, v in compound.items():
                setattr(self, k, frozenset(v))  # attach at desired mountpoint

            if overlay:
                return self.overlay(overlay)
            return self

        def overlay(self, target, override=False):

            ''' Build or update this :py:class:`Interpreter`'s
                understanding of the current ``compound`` profile.

                :param target: Foreign :py:class:`EventProfile`
                               descendent to merge.

                :keyword override: Bool indicating whether the
                                   overlayed profile should take
                                   override priority. Defaults to
                                   ``False``.

                :returns: ``self``, for method chainability. '''

            ## prepend target and build flattened chain
            chain = []

            for parent in target:
                if isinstance(parent, type) and issubclass(parent, AbstractProfile):
                    chain += [parent]
                    if hasattr(target, '__chain__'):
                        chain += target.__chain__

            self.__chain__ = tuple(chain)
            return self

        __call__ = overlay

    def __new__(cls, name, bases, properties):

        ''' Construct a new :py:class:`Profile` descendent.

            :param name: Profile name to dynamically construct.
            :param bases: Base classes for target profile class.
            :param properties: Class-level property mappings.
            :raises RuntimeError: In the case of an invalid spec parent.
            :returns: Constructed :py:class:`Profile` descendent. '''

        if name not in frozenset(('Profile', 'AbstractProfile')):  # must filter by string, `AbstractProfile` will fail

            ## grab specs
            spec = {}
            for spec_name, spec_klass in filter(lambda x: not x[0].startswith('_'), properties.iteritems()):

                # look for protocol binding subclasses
                if isinstance(spec_klass, type) and issubclass(spec_klass, meta.ProtocolBinding):

                    # pluck parent and specification structure
                    parent, subspec = spec_klass.__bases__[0], spec_klass

                    # grab builder and build
                    if parent not in cls.Interpreter._builders:
                        if parent.__bases__[0] not in cls.Interpreter._builders:
                            raise RuntimeError('Encountered invalid specification parent'
                                               ' "%s" in strict subclass "%s".' % (spec_klass, name))
                        else:
                            parent = parent.__bases__[0]

                    # add to specs, initializing the parent as we go
                    if parent not in spec:
                        spec[parent] = []

                    spec[parent].append((subspec, spec_klass, True))

            ## set up class internals and build
            _klass = {
                '__interpreter__': cls.Interpreter(name, spec).build(overlay=bases),
                '__bases__': bases,
                '__name__': name,
                '__chain__': tuple(),
                '__path__': properties.get('__module__', 'policy.base'),
                '__definition__': '.'.join(properties.get('__module__', 'policy.base').split('.') + [name])
            }

            if 'refcode' in properties:
                _klass['refcode'] = properties['refcode']

            ## substitute our class definition
            properties = _klass

        dynklass = super(cls, cls).__new__(cls, name, bases, properties)
        return cls.register(dynklass)

    def _mro(cls):

        ''' Calculate method resolution order for a
            :py:class:`Profile` descendent.

            :returns: Calculated MRO path for a non-meta
                      :py:class:`Profile` descendent. '''

        return tuple([cls] + [i for i in cls.__bases__])

    @classmethod
    def register(cls, dynamic_klass):

        ''' Register a newly-factoried `Profile` meta-descendent.

            :param dynamic_klass: Dynamically-factoried class, produced
            by :py:meth:`Profile.__new__`.

            :returns: The dynamic class that was passed-in and added
            to the local registry (at :py:attr:`Profile.registry`),
            such that method chaning takes place on the :py:class:`Profile`
            factoried rather than the meta-descendent. '''

        if dynamic_klass.__name__ != 'AbstractProfile':
            cls.registry[(dynamic_klass.__path__, dynamic_klass.__name__)] = dynamic_klass
        return dynamic_klass


## AbstractProfile
# Enforces application of metaclasses and intercepts construction calls.
class AbstractProfile(object):

    ''' Abstract :py:class:`EventProfile` parent that enforces
        proper use of the :py:class:`Profile` metaclass, and
        prevents incorrect construction / instantiation. '''

    __metaclass__ = Profile

    def __new__(cls, *args, **kwargs):

        ''' Disallow instantiation of :py:class:`AbstractProfile`
            descendents, as they are meant to be structural schema
            and not ephemeral objects.

            :param *args: Positional argument rollup.
            :param **kwargs: Keyword argument rollup.
            :raises: :py:exc:`NotImplementedError`, always. '''

        raise NotImplementedError('Cannot instantiate abstract'
                                  'class `%s`.' % cls.__name__)

    @util.classproperty
    def primitives(cls):

        ''' For each configured primitive extension
            binding, delegate to the embedded local
            :py:class:`Interpreter`, and yield each,
            one-at-a-time.

            :returns: Yields each configured primitive
            binding, one-at-a-time. '''

        for compound in [cls] + list(cls.__interpreter__.__chain__):
            for primitive in compound.__interpreter__.primitives:
                yield primitive

    @util.classproperty
    def parameters(cls):

        ''' For each configured parameter attached to this
            profile, delegate to the embedded local
            :py:class:`Interpreter`, and yield each, one
            at a time.

            :returns: Yields each configured :py:class:`Parameter`,
            one-at-a-time. '''

        for compound in [cls] + list(cls.__interpreter__.__chain__):
            for group in compound.__interpreter__.parameters:
                for parameter in group:
                    yield parameter

    @util.classproperty
    def attributions(cls):

        ''' For each configured attribution attached to this
            profile, delegate to the embedded local
            :py:class:`Interpreter`, and yield each, one
            at a time.

            :returns: Yields each configured :py:class:`Attribution`,
            one-at-a-time. '''

        for compound in [cls] + list(cls.__interpreter__.__chain__):
            for attribution in compound.__interpreter__.attributions:
                yield attribution

    @util.classproperty
    def aggregations(cls):

        ''' For each configured aggregation attached to this
            profile, delegate to the embedded local
            :py:class:`Interpreter`, and yield each, one
            at a time.

            :returns: Yields each configured :py:class:`Aggregation`,
            one-at-a-time. '''

        for compound in [cls] + list(cls.__interpreter__.__chain__):
            for aggregation in compound.__interpreter__.aggregations:
                yield aggregation

    @util.classproperty
    def integrations(cls):

        ''' For each configured integration attached to this
            profile, delegate to the embedded local
            :py:class:`Interpreter`, and yield each, one
            at a time.

            :returns: Yields each configured :py:class:`Integration`,
            one-at-a-time. '''

        for compound in [cls] + list(cls.__interpreter__.__chain__):
            for integration in compound.__interpreter__.integrations:
                yield integration
