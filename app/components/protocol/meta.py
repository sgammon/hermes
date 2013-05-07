# -*- coding: utf-8 -*-

'''

Components: Meta Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# stdlib
import config

# apptools util
from apptools.util import debug
from apptools.util import decorators
from apptools.util import datastructures


## Definition - metaclass for definition classes.
class Definition(type):

    ''' Metaclass for protocol definitions. '''

    registry = {}

    _config_path = 'api.components.protocol.Definition'

    def __new__(cls, name, bases, properties):

        ''' Factory a new `Definition` subclass. '''

        # split up properties
        _original_definition, _nonspecial_properties = frozenset(properties.keys()), {k: v for k, v in properties.iteritems() if not k.startswith('__')}

        # examine bindings, group options in descriptors
        _binding_config = {}
        for k, v in filter(lambda x: isinstance(x[1], tuple), _nonspecial_properties.iteritems()):
            _binding_config[k] = v[1]  # map config into `_binding_config`
            _nonspecial_properties[k] = v[0]  # extract property value

        # reorganize internals to freeze properties
        mapping = {

            '__slots__': tuple(),  # freeze property access, make class properties read-only
            '__config__': _binding_config,  # holds binding config options, passed as a dictionary in tuple position 2
            '__parent__': None,  # map to the direct parent of this definition - in terms of def path
            '__lookup__': frozenset(_nonspecial_properties.keys()),  # mapped forward lookup for keys
            '__reverse__': frozenset(_nonspecial_properties.values()),  # mapped reverse lookup for values
            '__override__': None,  # map to the definition this overrides, if any
            '__bindings__': _nonspecial_properties,  # original bindings from class definition block
            '__definition__': name,  # fully-qualified definition path of the new class

        }

        # update with special properties inherited from subclasses
        mapping.update({i: properties[i] for i in (_original_definition - mapping['__lookup__'])})

        # update with bindings
        mapping.update(_nonspecial_properties)

        #import pdb; pdb.set_trace()

        # construct new `Definition` class on-the-fly
        return super(cls, cls).__new__(cls, name, bases, mapping)

    def mro(cls):
    
        ''' Hook for generating a definition's MRO. '''

        # register definition and delegate to parent [MRO format: (<cls>, <ancestor 1>, <ancestor n>...)]
        return tuple([cls.register(cls)] + [i for i in filter(lambda x: x is not None, cls._ancestry)])

    @decorators.classproperty
    def _ancestry(cls):

        ''' Generate the ancestry tree for a `Definition`. '''

        _parent = cls
        while _parent is not None:
            _parent = _parent.__dict__.get('__parent__')
            yield _parent

    def register(cls, target):

        ''' Register a given definition in the definition registry. '''

        # register in local registry
        cls.registry[cls.__name__] = (cls.__dict__['__parent__'], cls)
        return cls

    def __repr__(cls):

        ''' Generate a string representation of a `Definition`. '''

        return '<Definition "%s.%s">' % (cls.__module__, cls.__name__)

    @classmethod
    def __getattr__(cls, name):

        ''' Retrieve a binding value. '''

        if name in cls.__lookup__:
            return cls.__bindings__[name]
        return None

    @classmethod
    def __setattribute__(cls, name, value):

        ''' Disallow changing attributes on `Definition` classes. '''

        raise AttributeError('Cannot set attributes on `Definition` classes at runtime.')

    __setattr__ = __setattribute__

    @decorators.classproperty
    def config(cls):

        ''' Named config pipe. '''

        return config.config.get(cls._config_path, {'debug': True})

    @decorators.classproperty
    def logging(cls):

        ''' Named logging pipe. '''

        _psplit = cls._config_path.split('.')
        return debug.AppToolsLogger(path='.'.join(_psplit[0:-1]), name=_psplit[-1])._setcondition(cls.config.get('debug', True))


## ProtocolDefinition - parent class for protocol definitions
class ProtocolDefinition(object):

    ''' Defines an element or component of a protocol. '''

    __metaclass__ = Definition

    def __new__(cls, *args, **kwargs):

        ''' Construct a new ProtocolDefinition subclass. '''

        raise RuntimeError('`Definition` classes are designed to be used at the class-level only, and are therefore restricted from instantiation.')
