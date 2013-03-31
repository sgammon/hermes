# -*- coding: utf-8 -*-

'''

Hermes: Exceptions

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''


## Top-level Error Classes
class Error(Exception): ''' Top-level Hermes error. '''
class ClientError(Error): ''' Error that occurred because of a client-side slip-up. '''
class PlatformError(Error): ''' Platform (server-side)-related errors that occur in APIs or handlers. '''

## Tracker Errors
class TrackerError(PlatformError): ''' Error that occurred within the Tracker subsystem. '''
class EventError(ClientError): ''' Error that occurred because of improper event structure. '''
class InvalidSentinel(EventError): ''' Indicates that a URL came through in non-debug mode without a sentinel key. '''

## API Errors
class APIError(PlatformError): ''' Error that occurred within ProtoRPC-backed RPC subsystems. '''
