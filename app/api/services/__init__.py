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

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Base Imports
import config
import webapp2

# apptools util
from apptools.util import debug

# apptools services
try:
    # new, service layer 2.0
    from apptools import rpc  # pragma: no cover
except:
    # fallback to old apptools servicelayer
    from apptools import services as rpc  # pragma: no cover


__all__ = ['event', 'pubsub', 'raw', 'tracker', 'harness']
