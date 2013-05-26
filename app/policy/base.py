# -*- coding: utf-8 -*-

'''

Base Policy

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

## protocol bindings
from protocol import meta
from protocol import http
from protocol import intake
from protocol import builtin
from protocol import timedelta
from protocol import environment

## protocol extensions
from protocol import parameter
from protocol import decorators
from protocol import integration
from protocol import attribution
from protocol import aggregation


## Constants
_DEFAULT_COOKIE_NAME = "_amp"

# Default attribution / aggregation lookback window
_DEFAULT_LOOKBACK = (timedelta.TimeWindow.ONE_DAY,
                     timedelta.TimeWindow.ONE_WEEK,
                     timedelta.TimeWindow.TWO_WEEKS,
                     timedelta.TimeWindow.THREE_WEEKS,
                     timedelta.TimeWindow.FOREVER)


## Profile
# Metaclass that provides structure for overridable profiles.
class Profile(type):

    ''' Abstract :py:class:`EventProfile` metaclass that provides
        structure for overridable profiles and enforces strict
        schema rules.

        An encapsulated class at :py:attr:`Profile.Interpreter`
        is used to read, merge, and export profile structures
        defined via :py:class:`EventProfile`-subclasses. '''

    ## Interpreter
    # Manages interpretation and merging of `Profile` descendents.
    class Interpreter(object):

        ''' Manages interpretation and merging of `Profile`
            descendents, and contains utility functions to
            break each discrete component down into an
            element in a virtual ``AST``-like structure. '''

        __slots__ = ('__tree__', '__interpreted__', '__compound__',
                     '__profile__', '__aggregations__', '__attributions__',
                     '__parameters__', '__integrations__')

        ## == Internals == ##
        def __init__(self, specs):

            ''' Instantiate a new ``Interpreter``, and attach
                the given ``profile`` for future work.

                :param profile: :py:class:`EventProfile` subclass
                                to interpret or merge.

                :returns: Nothing, this is a constructor. '''

            self.__profile__ = specs
            print "!!! Interpreter fired up. Profile dump to follow. !!!"
            for k, v in specs.iteritems():
                print "---%s:" % k
                for bundle in v:
                    spec, flag = bundle
                    print "   ---%s" % spec
                print ""

        def _build_paramgroup(self, group, inline=True):

            ''' Build a ``ParameterGroup`` object from a direct
                subclass, embedded in a :py:class:`EventProfile`
                definition.

                :param group: The :py:class:`ParameterGroup`
                              subclass to compile.

                :return: An instantiated and properly filled-out
                        :py:class:`ParameterGroup` object. '''

            print "Built(ParamGroup): %s" % group
            return group

        def _build_integration(self, spec, inline=True):

            ''' Build an ``Integration`` object from a
                specification encountered in a subclass of
                :py:class:`EventProfile`.

                :param spec: Class structure and specification, as
                             found in the encapsulating
                             :py:class:`EventProfile`.

                :keyword inline: Indicates that this is a subclass
                                   defined inline in an encapsulating
                                   :py:class:`EventProfile`. Defaults
                                   to ``True``.

                :returns: An instantiated and properly filled-out
                          :py:class:`IntegrationGroup` object. '''

            print "Built(Integration): %s" % spec
            return spec

        def _build_attribution(self, spec, compound=False):

            ''' Build an ``Attribution`` or ``CompoundAttribution``
                from a specification encountered in a subclass of
                :py:class:`EventProfile`.

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

            print "Built(AttributionGroup): %s" % spec
            return spec

        def _build_aggregation(self, spec, compound=False):

            ''' Build an ``Aggregation`` or ``CompoundAggregation``
                from a specification encountered in a subclass of
                :py:class:`EventProfile`.

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

            print "Built(AggregationGroup): %s" % spec
            return spec

        _builders = {
            integration.Integration: ('integrations', _build_integration),
            attribution.Attribution: ('attributions', _build_attribution),
            aggregation.Aggregation: ('aggregations', _build_aggregation),
            parameter.ParameterGroup: ('parameters', _build_paramgroup)
        }

        ## == Public Methods == ##
        def build(self):

            ''' Build a :py:class:`EventProfile` descendent
                into a fully-structured object.

                :returns: ``self``, for method chainability. '''

            compound = {}
            for (parent, subspecs) in self.__profile__.iteritems():
                for spec, flag in subspecs:
                    attr, builder = self._builders[parent]
                    compound[attr] = builder(self, spec, flag)

            self.__compound__ = compound

            print "!!! Interpreter built compound object. Compound dump to follow. !!!"
            for k, v in self.__compound__.items():
                print "%s: %s" % (k, v)

            return self

        def overlay(self, target):

            ''' Build or update this :py:class:`Interpreter`'s
                understanding of the current ``compound`` profile.

                :param target: Foreign :py:class:`EventProfile`
                               descendent to merge.

                :returns: ``self``, for method chainability. '''

            return self

        __call__ = overlay

    def __new__(cls, name, bases, properties):

        ''' Construct a new :py:class:`Profile` descendent.

            :param name:
            :param bases:
            :param properties:
            :raises RuntimeError:
            :returns: '''

        if name not in frozenset(('Profile', 'AbstractProfile')):  # must filter by string, `AbstractProfile` comes through here

            ## grab specs
            spec = {}
            for spec_name, spec_klass in filter(lambda x: not x[0].startswith('_'), properties.iteritems()):

                # look for protocol binding subclasses
                if isinstance(spec_klass, type) and issubclass(spec_klass, meta.ProtocolBinding):

                    # pluck parent and specification structure
                    parent, subspec = spec_klass.__bases__[0], spec_klass

                    # add to specs, initializing the parent as we go
                    if parent not in spec:
                        spec[parent] = []

                    # grab builder and build
                    if parent not in cls.Interpreter._builders:
                        raise RuntimeError('Encountered invalid specification parent'
                                           ' "%s" in strict subclass "%s".' % (spec_klass, name))

                    spec[parent].append((subspec, True))

            ## set up class internals and build
            _klass = {
                '__interpreter__': cls.Interpreter(spec).build()
            }

            ## substitute our class definition
            properties = _klass

        return super(cls, cls).__new__(cls, name, bases, properties)

    def _mro(cls):

        ''' Calculate method resolution order for a
            :py:class:`Profile` descendent. '''

        pass


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


## EventProfile
# Default Event Profile.
class EventProfile(AbstractProfile):

    ''' Root concrete :py:class:`EventProfile` class. This is
        the eventual inheritance target for all ``EventProfile``
        classes. '''

    class Base(parameter.ParameterGroup):

        ''' Parameter group for base tracker parameters. '''

        # Sentinel: flag indicating that the hit URL was generated by our systems.
        sentinel = bool, {
            'policy': parameter.ParameterPolicy.ENFORCED,
            'source': http.DataSlot.PARAM,
            'name': builtin.TrackerProtocol.SENTINEL,
            'category': parameter.ParameterType.INTERNAL
        }

        # Type: represents the type of hit, such as "impression" or "click".
        type = str, {
            'policy': parameter.ParameterPolicy.REQUIRED,
            'source': http.DataSlot.PARAM,
            'name': builtin.TrackerProtocol.TYPE,
            'category': parameter.ParameterType.INTERNAL,
            'aggregations': [
                aggregation.Aggregation(name='events-by-type', interval=_DEFAULT_LOOKBACK)
            ]
        }

        # Tracker: represents the ID of the parent tracker for the current hit.
        tracker = str, {
            'policy': parameter.ParameterPolicy.REQUIRED,
            'source': http.DataSlot.PARAM,
            'name': builtin.TrackerProtocol.TRACKER,
            'category': parameter.ParameterType.AMPUSH,
            'aggregations': [
                aggregation.Aggregation(name='events-by-tracker', interval=_DEFAULT_LOOKBACK)
            ]
        }

        # Provider: represents the ID string of the provider of this hit.
        provider = str, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'source': http.DataSlot.PARAM,
            'name': builtin.TrackerProtocol.PROVIDER,
            'category': parameter.ParameterType.INTERNAL,
            'aggregations': [
                aggregation.Aggregation(name='events-by-provider', interval=_DEFAULT_LOOKBACK)
            ]
        }

        # Contract: represents the contract scope which this hit should be recorded for.
        contract = str, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'source': http.DataSlot.PARAM,
            'name': builtin.TrackerProtocol.CONTRACT,
            'category': parameter.ParameterType.AMPUSH,
            'aggregations': [
                aggregation.Aggregation(name='events-by-contract', interval=_DEFAULT_LOOKBACK)
            ]
        }

    class Environment(parameter.ParameterGroup):

        ''' Parameter group for client browser environment. '''

        # OS: The operating system the browser is running in.
        os = str, {
            'policy': parameter.ParameterPolicy.PREFERRED,
            'source': http.DataSlot.PARAM,
            'name': environment.BrowserEnvironment.OS,
            'category': parameter.ParameterType.DATA,
            'aggregations': [
                aggregation.Aggregation(name='hits-by-os', interval=_DEFAULT_LOOKBACK)
            ]
        }

        # Arch: The underlying architecture of the host operating system (i.e. "x86-64").
        arch = str, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'source': http.DataSlot.PARAM,
            'name': environment.BrowserEnvironment.ARCH,
            'category': parameter.ParameterType.DATA,
        }

        # Vendor: The author of the browser being used (i.e. "Google" for Chrome).
        vendor = str, {
            'policy': parameter.ParameterPolicy.PREFERRED,
            'source': http.DataSlot.PARAM,
            'name': environment.BrowserEnvironment.VENDOR,
            'category': parameter.ParameterType.DATA
        }

        # Browser: The software-name of the browser being used (i.e. "Safari" for Safari).
        browser = str, {
            'policy': parameter.ParameterPolicy.PREFERRED,
            'source': http.DataSlot.PARAM,
            'name': environment.BrowserEnvironment.BROWSER,
            'category': parameter.ParameterType.DATA,
            'aggregations': [
                aggregation.Aggregation(name='hits-by-browser', interval=_DEFAULT_LOOKBACK)
            ]
        }

    class Consumer(parameter.ParameterGroup):

        ''' Parameter group for identifying unique consumers. '''

        # Fingerprint: The consumer profile fingerprint, either encountered or created.
        fingerprint = str, {
            'policy': parameter.ParameterPolicy.SPECIAL,
            'source': http.DataSlot.COOKIE,
            'name': _DEFAULT_COOKIE_NAME,
            'category': parameter.ParameterType.INTERNAL,
            'attributions': [
                attribution.Attribution(name='hits-to-cookies')
            ]
        }

    class System(parameter.ParameterGroup):

        ''' Parameter group for system state/configuration. '''

        channel = int, {
            'policy': parameter.ParameterPolicy.SPECIAL,
            'source': http.DataSlot.HEADER,
            'name': 'XAF-Channel',
            'category': parameter.ParameterType.INTERNAL,
            'binding': intake.InputChannel
        }
