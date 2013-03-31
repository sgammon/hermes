# -*- coding: utf-8 -*-

'''

Components: Meta Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''


## Definition - metaclass for definition classes.
class Definition(type):

	''' Metaclass for protocol definitions. '''

	def __new__(cls, name, types, mapping):

		''' Factory a new protocol definition. '''

		return type(name, types, mapping)


## ProtocolDefinition - parent class for protocol definitions
class ProtocolDefinition(object):

	''' Defines an element or component of a protocol. '''

	__metaclass__ = Definition

	def __new__(cls, *args, **kwargs):

		''' Construct a new ProtocolDefinition subclass. '''

		if not hasattr(cls, '__metaclass__'):
			cls.__metaclass__ = Definition

		return cls(*args, **kwargs)
