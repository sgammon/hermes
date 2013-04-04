# -*- coding: utf-8 -*-

'''

API: Services

This package exports classes for use as ProtoRPC services. Services defined
here and registered in config at `config.services` will automatically appear
(unless hidden) in the JavaScript context.

The AppTools service layer is integrated with AppTools JS and uses a simple,
custom JSON-wire format to dispatch RPC services. ProtoRPC (the underlying
plumbing for API dispatch and serialization) allows compatibility outside
of standard HTTP scope - so, service methods could theoretically be dispatched
over WebSockets or other exotic transports without code changes.

The services listed here are dependent on Message classes, that structure
the Request/Response flow. AppTools models happen to make great Message classes.
Messages that must be custom-built live in `messages`.

-sam (<sam.gammon@ampush.com>)

'''
