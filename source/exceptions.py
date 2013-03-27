
class Error(Exception): ''' Top-level Hermes error. '''

class PlatformError(Error): ''' Platform (server-side)-related errors. '''
class ClientError(Error): ''' Error that occurred because of a client-side slip-up. '''

class TrackerError(PlatformError): ''' Error that occurred within the Tracker subsystem. '''
class APIError(PlatformError): ''' Error that occurred within ProtoRPC-backed RPC subsystems. '''
class EventError(ClientError): ''' Error that occurred because of improper event structure. '''
class InvalidSentinel(EventError): ''' Indicates that a URL came through in non-debug mode without a sentinel key. '''
