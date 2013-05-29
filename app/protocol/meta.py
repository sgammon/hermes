# -*- coding: utf-8 -*-

"""
Protocol: Meta Bindings

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

"""pylint option block-disable"""

try:
    import config; _APPCONFIG = True
except ImportError:
    _APPCONFIG = False  # pragma: no cover

# apptools util
from apptools.util import debug
from apptools.util import decorators
from apptools.util import datastructures


class Definition(object):

    ''' Definition. '''

    __lookup__ = frozenset()
    _config_path = 'api.components.protocol.Definition'

    class __metaclass__(type):

        ''' Embedded metaclass - enforces ABC compliance and
            packages properties into compound policy definition
            classes. '''

        __owner__ = 'Definition'  # alias produced classes to this owner
        _definition_registry = {}  # Holds encountered ``Definition`` subclasses.

        def __new__(cls, name, bases, properties):

            ''' Initialize this :py:class:`Definition`. '''

            # split up properties
            _original_definition = frozenset(properties.keys())
            _nonspecial_properties = {k: v for k, v in properties.iteritems() if not k.startswith('_')}
            _prop_lookup, _value_lookup, _prop_data, _value_data, _binding_config = set(), set(), [], [], {}
            _special_properties = {k: v for k, v in properties.iteritems() if k.startswith('_')}

            # examine bindings, group options in descriptors
            if properties.get('__frozen__', False) is False:
                for k, v in _nonspecial_properties.iteritems():
                    if isinstance(v, tuple):
                        _binding_config[k] = v[1]  # map config into `_binding_config`
                        _prop_lookup.add(k)  # add key to property lookup
                        _prop_data.append(k)  # add key (positional)
                        _value_data.append(v)  # add value (positional)

            else:
                # resolve, hash, and enforce uniqueness for mappings
                for key, value in _nonspecial_properties.items():
                    if isinstance(value, tuple):
                        ## this is a mapping, not an enum. zip and break.
                        _prop_data.append(key)
                        _value_data.append(value)
                        continue
                    if key not in _prop_lookup and key not in _value_lookup:
                        _prop_lookup.add(key)
                        _prop_data.append(key)
                        if value not in _value_lookup and value not in _prop_lookup:
                            _value_lookup.add(value)
                            _value_data.append(value)
                            continue
                        else:
                            offender, otype = value, 'value'
                    else:
                        offender, otype = key, 'key'
                    context = (otype, offender, '.'.join(properties.get('__module__', '__main__').split('.') + [name]))
                    raise ValueError('Value (`%s`: "%s") was repeated more than once as a `key` or `value`'
                                     'in a ``Definition`` subclass ("%s").' % context)

            # reorganize internals to freeze properties
            mapping = {

                #'__slots__': tuple(),  # freeze property access, make class properties read-only
                '__config__': _binding_config,  # holds binding config options, passed as a dictionary in tuple position 2
                '__parent__': None,  # map to the direct parent of this definition - in terms of def path
                '__lookup__': _prop_lookup,  # mapped forward lookup for keys
                '__value_lookup__': _value_lookup,  # mapped reverse lookup for values
                '__forward__': tuple(_prop_data),  # ordered, mapped prop names
                '__reverse__': tuple(_value_data),  # ordered, mapped prop values
                '__override__': None,  # map to the definition this overrides, if any
                '__definition__': name  # fully-qualified definition path of the new class

            }

            # update with special properties inherited from subclasses
            mapping.update({i: properties[i] for i in (_original_definition - mapping['__lookup__'])})

            # update with bindings
            mapping.update(_nonspecial_properties)
            mapping.update(_special_properties)

            # construct new `Definition` class on-the-fly
            klass = super(cls, cls).__new__(cls, name, bases, mapping)
            datastructures.BidirectionalEnum.register(klass)

            # preload config / logging
            klass._config, klass._logging

            return cls._register_definition(klass)

        @classmethod
        def _register_definition(cls, target):

            ''' Register a given definition in the definition registry. '''

            # register in local registry
            cls._definition_registry[target.__name__] = (target.__dict__['__parent__'], target)
            return target

        def __repr__(self):

            ''' Generate a string representation of a `Definition`. '''

            return '%s(path=%s, name=%s)' % (self.__owner__, self.__module__, self.__name__)

        def forward_resolve(self, name):

            ''' Resolve an enumerated value by key. '''

            if name in self.__lookup__:
                return self.__reverse__[self.__forward__.index(name)]
            raise AttributeError('Definition has no binding for key "%s".' % name)

        def __serialize__(self):

            ''' Flatten down into a structure suitable for storage/transport. '''

            return dict(zip(self.__forward__, self.__reverse__))

    @decorators.memoize
    @decorators.classproperty
    def _config(cls):

        ''' Named config pipe. '''

        if _APPCONFIG:
            return config.config.get(cls._config_path, {'debug': True})
        return {'debug': True}

    @decorators.memoize
    @decorators.classproperty
    def _logging(cls):

        ''' Named logging pipe. '''

        _psplit = cls._config_path.split('.')
        return debug.AppToolsLogger(**{
            'path': '.'.join(_psplit[0:-1]),
            'name': _psplit[-1]})._setcondition(cls._config.get('debug', True))


class ProtocolBinding(Definition):

    ''' ProtocolBinding. '''

    # == Object Members == #
    __config__ = None
    __frozen__ = False
    __subtype__ = None

    # == Internals == #
    def __init__(self, subtype=None, **kwargs):

        ''' Initialize this :py:class:`ProtocolBinding`,
            optionally with a specified ``subtype``.

            :param subtype: Name of a subtype to factory
                            for this :py:class:`ProtocolBinding`.

            :param kwargs: Configuration ``dict`` for this
                           :py:class:`ProtocolBinding`, in the
                           form of keyword arguments.

            :returns: Nothing, as this is a constructor. '''

        print "%s(%s, %s)" % (self.__class__.__name__, subtype, kwargs)
        self.__subtype__, self.__config__ = subtype, kwargs


class ProtocolDefinition(Definition):

    ''' ProtocolDefinition. '''

    __frozen__ = True

    @classmethod
    def reverse_resolve(cls, value):

        ''' Resolve an enumerated key by value. '''

        if value in cls.__value_lookup__:  # pylint: disable-msg=E1101
            return cls.__forward__[cls.__reverse__.index(value)]
        raise KeyError('Definition has no binding for value "%s".' % value)

    __getitem__ = reverse_resolve
