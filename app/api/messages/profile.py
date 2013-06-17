# -*- coding: utf-8 -*-

'''
Holds structured :py:class:`protorpc.Message` classes for expressing
:py:class:`policy.core.Policy` trees, their descendents, and attached
:py:class:`procotol.meta.ProtocolDefinition` / :py:class:`procotol.meta.ProtocolBinding`
classes.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# apptools rpc
from apptools import rpc


# Definition
# Expresses a :py:class:`protocol.meta.ProtocolDefinition`.
class Definition(rpc.messages.Message):

    ''' Expresses a :py:class:`protocol.meta.ProtocolDefinition`
        class as a message, for use in the API service layer. '''

    pass  # STUBBED


# Binding
class Binding(rpc.messages.Message):

    ''' Expresses a :py:class:`protocol.meta.ProtocolBinding`
        class as a message, for use in the API service layer. '''

    pass  # STUBBED


# Policy
class Policy(rpc.messages.Message):

    ''' Expresses a :py:class:`policy.core.Policy` class
        (or valid descendent) as a message, for use in the
        API service layer. '''

    pass  # STUBBED
