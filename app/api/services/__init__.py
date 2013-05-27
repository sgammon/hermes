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
    from apptools import rpc
except:
    # fallback to old apptools servicelayer
    from apptools import services as rpc


## APIService - abstract parent for all service APIs
class APIService(rpc.Service):

    ''' Abstract parent class for all Hermes API services. '''

    _config_path = 'hermes.api.services.APIService'

    @webapp2.cached_property
    def config(self):

        ''' Cached access to `PubSubService` config. '''

        return config.config.get(self._config_path, {'debug': False})

    @webapp2.cached_property
    def logging(self):

        ''' Cached access to dedicated log pipe. '''

        path = self._config_path.split('.')
        return debug.AppToolsLogger(path='.'.join(path[0:-1]), name=path[-1])._setcondition(self.config.get('debug'))
