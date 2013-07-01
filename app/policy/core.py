# -*- coding: utf-8 -*-

'''

Policy Core

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# stdlib
import os

# protocol bindings
from protocol import meta

# protocol extensions
from protocol import transport
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

        ## == Data Members == ##
        primitives = tuple()
        parameters = tuple()
        aggregations = tuple()
        attributions = tuple()
        integrations = tuple()
        configuration = tuple()

        ## == Internal Members == ##
        __tree__ = tuple()
        __chain__ = tuple()
        __subtype__ = None
        __profile__ = None

        ## == Internals == ##
        def __init__(self, name, specs=tuple()):

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
                :py:class:`EventProfile`) that we are processing
                for, so we can inform sub-objects.

                :param group: The :py:class:`ParameterGroup`
                subclass to compile.

                :param klass: Encapsulating policy definition
                class that we're building for.

                :return: An instantiated and properly filled-out
                        :py:class:`ParameterGroup` object. '''

            # overlay parameter path, init params list
            parameters, mainconfig = [], {
                'definition': {
                    'path': '.'.join(group.__module__.split('.') + [self.__subtype__]),
                    'name': group.__name__
                }
            }

            _parent_policy = policy.__bases__[0]

            # do we need a pool of parent properties?
            param_pool, local_pool, parent_pool = (
                {},
                {i: group.__dict__[i] for i in group.__forward__},
                {param.name: param for param in _parent_policy.parameters}
            )

            # build and initialize parameters
            for param, config in local_pool.iteritems():

                # resolve parent parameter
                current_param = None
                parent_path = '.'.join((mainconfig['definition']['name'], param.upper()))  # like `Base.PROVIDER`
                parent_param = None
                if policy.__bases__[0].__name__ != 'AbstractProfile':
                    parent_param = policy.__bases__[0].resolve_parameter(parent_path)


                # `OVERRIDE` mode - fully replace any parent declaration by the same name
                # `DECLARATION` mode - differential parameter-level mode - merge params by group
                if group.__mode__ in (parameter.ParamDeclarationMode.OVERRIDE,
                                      parameter.ParamDeclarationMode.DECLARATION):

                    if isinstance(config, tuple):  # we're configuring schema
                        basetype, config = config

                        if group.__mode__ is parameter.ParamDeclarationMode.OVERRIDE:
                            basevalue = None
                        else:
                            basevalue = parent_param.basevalue if parent_param else None

                        # update with mainconfig, build and append
                        config.update(mainconfig)

                    else:  # simple basetype mapping
                        basetype, config, basevalue = config, {}, None

                        # update with mainconfig, build and append
                        config.update(mainconfig)

                    # construct our new parameter and add to the parameter pool
                    param_pool[param] = current_param = parameter.Parameter(*(
                        policy,
                        parent_param,
                        mainconfig['definition']['name'],
                        param,
                        basetype,
                        basevalue),
                        **config)


                # `VALUES` mode - should simply fill in values for each listed parameter
                elif group.__mode__ is parameter.ParamDeclarationMode.VALUES:

                    if isinstance(config, tuple):  # this is an error
                        raise TypeError('Cannot provide schema with @param.values decorator. Got: "%s".' % config)

                    if parent_param is not None:
                        basevalue, config = config, parent_param.config
                    else:
                        basevalue, config = config, {}

                    param_pool[param] = current_param = parameter.Parameter(*(
                        policy,
                        parent_param,
                        mainconfig['definition']['name'],
                        param,
                        parent_param.basetype,
                        basevalue),
                        **config)


                # `DIFFERENTIAL` mode - apply changes in this class to the parent and take the result
                elif group.__mode__ is parameter.ParamDeclarationMode.DIFFERENTIAL:

                    if isinstance(config, tuple):  # we're configuring schema
                        basetype, config = config
                        basevalue = parent_param.basevalue if parent_param else None

                    else:
                        if isinstance(config, type):  # simple basetype mapping
                            basetype, config, basevalue = config, {}, None

                        else:  # simple basevalue mapping
                            basetype, config, basevalue = parent_param.basetype, {}, config

                    _cfg = {}  # build config
                    if parent_param:
                        _cfg.update(parent_param.config)  # merge-in parent config
                    _cfg.update(mainconfig)  # merge-in group config
                    _cfg.update(config)  # merge-in local config

                    param_pool[param] = current_param = parameter.Parameter(*(
                        policy,
                        parent_param,
                        mainconfig['definition']['name'],
                        param,
                        parent_param.basetype if parent_param else basetype,
                        basevalue),
                        **_cfg)

                else:
                    raise RuntimeError('Invalid `ParameterGroup` specification mode. Got: "%s".' % group.__mode__)

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

            group = parameter.ParameterGroup(group.__name__, param_pool.values(), inline=inline)
            for param in group:
                param.set_group(group)
            return group

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

        def _build_configuration(self, policy, spec, klass, inline=False):

            ''' Build a ``Configuration`` object from a specification
                encountered in a subclass of :py:class:`EventProfile`. '''

            return spec

        _builders = {
            integration.Integration: ('integrations', _build_integration),
            attribution.Attribution: ('attributions', _build_attribution),
            aggregation.Aggregation: ('aggregations', _build_aggregation),
            parameter.ParameterGroup: ('parameters', _build_paramgroup),
            transport.TransportConfig: ('configuration', _build_configuration)
        }

        ## == Public Methods == ##
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
                    chain += ([parent] + list(parent.__interpreter__.__chain__))

            self.__chain__ = tuple(chain)
            return self

        def build(self, base_policy, overlay=None):

            ''' Build a :py:class:`EventProfile` descendent
                into a fully-structured object.

                :param base_policy:
                :param overlay:

                :returns: ``self``, for method chainability. '''

            # initialize compound structure
            compound = {
                'primitives': [],
                'parameters': [],
                'aggregations': [],
                'attributions': [],
                'integrations': [],
                'configuration': []
            }

            for (parent, subspecs) in self.__profile__.iteritems():
                for spec, flag in subspecs:
                    attr, builder = self._builders[parent]
                    compound[attr].append(builder(self, base_policy, spec, compound, flag))
                    compound['primitives'].append(spec)

            # assign locally
            for k, v in compound.iteritems():
                setattr(self, k, v)

            if overlay:
                return self.overlay(overlay)
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

                    spec[parent].append((spec_klass, True))

            ## set up class internals and build
            _klass = {
                '__interpreter__': cls.Interpreter(name, spec),
                '__bases__': bases,
                '__name__': name,
                '__chain__': tuple(),
                '__path__': properties.get('__module__', 'policy.base'),
                '__definition__': '.'.join(properties.get('__module__', 'policy.base').split('.') + [name])
            }

            if 'refcode' in properties:

                if isinstance(properties['refcode'], basestring):
                    _ref_code = properties['refcode'].lower().strip()

                elif isinstance(properties['refcode'], (frozenset, set, list, tuple)):
                    _multiref = []
                    for i in _ref_code:

                        if not isinstance(i, basestring):
                            raise TypeError('Cannot provide non-string `ref` for legacy tracking profile.'
                                            ' Got: "%s".' % str(i))

                        _multiref.append(i.lower().strip())

                    _ref_code = frozenset(_multiref)

                _klass['refcode'] = _ref_code

            ## substitute our class definition
            properties = _klass

            # build class and compile profile
            dynklass = super(cls, cls).__new__(cls, name, bases, properties)
            dynklass.__interpreter__.build(dynklass, overlay=bases)

        else:
            properties.update({
                '__interpreter__': cls.Interpreter(name),
                '__chain__': tuple(),
                '__path__': properties.get('__module__', 'policy.core'),
                '__definition__': '.'.join(properties.get('__module__', 'policy.base').split('.') + [name]),
                '__bases__': bases,
                '__name__': name
            })
            dynklass = super(cls, cls).__new__(cls, name, bases, properties)

        return cls.register(dynklass)

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

    ## == Public Properties == ##
    @util.classproperty
    def chain(cls):

        ''' Walk the :py:class:`Profile` inheritance
            chain of the locally-interpreted profile.

            :yields: Each ``link`` in the profile
            inheritance :py:attr:`self.__chain__`. '''

        for link in (cls.__interpreter__.__chain__ + cls.__bases__):
            if hasattr(link, '__interpreter__'):
                yield link

    @util.classproperty
    def primitives(cls):

        ''' Yield each primitive class attached to
            the locally-interpreted :py:class:`Profile`.

            :yields: Each class ``primitive``. '''

        for generator in (cls.parameters,
                          cls.aggregations,
                          cls.attributions,
                          cls.integrations):

            for primitive in generator:
                yield primitive

    @util.classproperty
    def parameters(cls):

        ''' For each configured parameter attached to this
            profile, delegate to the embedded local
            :py:class:`Interpreter`, and yield each, one
            at a time.

            :returns: Yields each configured :py:class:`Parameter`,
            one-at-a-time. '''

        for compound in [cls] + list(cls.chain):
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

        for compound in [cls] + list(cls.chain):
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

        for compound in [cls] + list(cls.chain):
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

        for compound in [cls] + list(cls.chain):
            for integration in compound.__interpreter__.integrations:
                yield integration

    @classmethod
    def resolve_parameter(cls, qualified_path):

        ''' Resolve a parameter object by its qualified
            definition path. '''

        split = qualified_path.lower().split('.')
        split[0] = split[0].capitalize()

        for block in cls.parameters:
            if block.group.name == split[0]:
                if block.name == split[1]:
                    return block
            continue
        return None  # explicit ``None`` if it couldn't be found
