# -*- coding: utf-8 -*-

'''

API: Handlers

This module contains the top level WebHandler, which is responsible for
responding to regular HTTP requests in a traditional HTTP request/response
cycle. All project handlers should inherit from this.

-sam (<sam.gammon@ampush.com>)

'''

# Base Imports
import os
import config
import hashlib

# Webapp2 Imports
import webapp2

# AppTools Imports
from apptools import core

# AppTools Util Imports
from apptools.util import json
from apptools.util import debug
from apptools.util import datastructures


## WebHanlder - parent class for all site request handler classes
class WebHandler(core.BaseHandler):

    ''' Handler for desktop web requests. '''

    # Preloader / Sessions
    session = None  # holds loaded/constructed session object
    preload = None  # holds preloaded template, if supported
    template = None  # string path to associated template

    # Config Paths
    _jinja2_config_path = 'webapp2_extras.jinja2'
    _handler_config_path = 'api.classes.WebHandler'
    _p_output_config_path = 'apptools.project.output'

    # RPC Transport Settings
    transport = {

        'endpoint': 'api.amp.sh',  # API endpoint (passed to client)
        'consumer': 'hermes-sandbox',  # API consumer name (logging/simple access control)
        'secure': True if not config.debug else False,  # whether to communicate over HTTPS

        'realtime': {  # realtime / websocket settings
            'enabled': False,  # enable/disable realtime
            'endpoint': None,  # endpoint for realtime sockets
            'secure': False  # whether to communicate over HTTPS
        }

    }

    ## ++ Internal Shortcuts ++ ##

    ## Debug Pipe
    @webapp2.cached_property
    def debug(self):

        ''' Shortcut to AppTools debugging utilities. '''

        return debug

    ## Logging Pipe
    @webapp2.cached_property
    def logging(self):

        ''' Named logging pipe / shortcut. '''

        return debug.AppToolsLogger(path='api.handlers', name='WebHandler')._setcondition(config.debug)

    ## Config Shortcuts
    @webapp2.cached_property
    def config(self):

        ''' Cached access to main config for this handler. '''

        return self._webHandlerConfig

    @webapp2.cached_property
    def _webHandlerConfig(self):

        ''' Cached access to this handler's config. '''

        return config.config.get(self._handler_config_path)

    @webapp2.cached_property
    def _jinjaConfig(self):

        ''' Cached access to Jinja2 base config. '''

        return config.config.get(self._jinja2_config_path)

    @webapp2.cached_property
    def _integrationConfig(self):

        ''' Cached access to this handler's integration config. '''

        return self._webHandlerConfig.get('integrations')

    @webapp2.cached_property
    def _outputConfig(self):

        ''' Cached access to base output config. '''

        return config.config.get(self._p_output_config_path)

    ## Internals
    @webapp2.cached_property
    def hostname(self):

        ''' Return proxied or request hostname. '''

        return self.request.host if not self.force_hostname else self.force_hostname

    @webapp2.cached_property
    def baseTransport(self):

        ''' Return a clean set of transport base settings. '''

        return {
            'secure': False,
            'endpoint': self.hostname,
            'consumer': 'apptools-sandbox',
            'scope': 'readonly',
            'realtime': {
                'enabled': False
            },
            'make_object': lambda x: self._make_services_object(x)
        }

    @webapp2.cached_property
    def computedTransport(self):

        ''' Overlay this handler's transport settings on the app's base settings and return. '''

        b = dict([(k, v) for k, v in self.baseTransport.items()])
        b.update(self.transport)
        return b

    @webapp2.cached_property
    def template_environment(self):

        ''' Return a new environment, because if we're already here it's not cached. '''

        return self.jinja2

    @webapp2.cached_property
    def jinja2(self):

        ''' Cached access to Jinja2. '''

        ## Patch in dynamic content support
        if hasattr(self, 'dynamicEnvironmentFactory'):
            return self._output_api.get_jinja(self.app, self.dynamicEnvironmentFactory)
        else:
            return self._output_api.get_jinja(self.app, self.jinja2EnvironmentFactory)

    def _preload_data(self):

        ''' Preloaded data support. '''

        self.logging.info('Data preloading currently disabled.')
        return self

    def _preload_template(self):

        ''' Preloaded template support. '''

        if hasattr(self, 'template') and getattr(self, 'template') not in frozenset(['', None, False]):
            self.preload_template(self.template)
        return self

    def _make_services_object(self, services):

        ''' Make a dict suitable for JSON representing an API service. '''

        return [[
            service,
            cfg['methods'],
            opts
        ] for service, action, cfg, opts, in services['services_manifest']]

    def _bindRuntimeTemplateContext(self, context):

        ''' Bind a bunch of utils-n-stuff at runtime. '''

        context.update({

            '_meta': config.config.get('apptools.output.meta'),
            '_opengraph': config.config.get('apptools.output.meta').get('opengraph', {}),
            'handler': self,
            'transport': {
                'services': self.computedTransport,
                'realtime': {
                    'enabled': False
                }
            },
            'security': {
                'current_user': self.current_user
            }

        })

        return super(WebHandler, self)._bindRuntimeTemplateContext(context)

    ## ++ External Methods ++ ##
    def initialize(self, request, response):

        ''' Initialize this handler. '''

        super(core.BaseHandler, self).initialize(request, response)
        return self

    def dispatch(self):

        ''' Dispatch a response for a given request using this handler. '''

        try:
            _super = super(WebHandler, self)
            response = _super.dispatch()

            if isinstance(response, basestring):
                self.response.write(response)

            elif isinstance(response, webapp2.Response):
                self.response = response

            elif response is None:
                response = self.response

        except Exception, e:

            if config.debug:
                raise
            else:
                self.handle_exception(e)

        return self.response

    ## Render APIs
    def render(self, *args, **kwargs):

        ''' If supported, pass off to dynamic render, which rolls-in support for editable content blocks. '''

        if hasattr(self, 'content'):
            return self.content.render(*args, **kwargs)
        else:
            return super(WebHandler, self).render(*args, **kwargs)

    ## HTTP Methods
    def head(self):

        ''' Run GET, if defined, and return the headers only. '''

        response = None
        if hasattr(self, 'get'):
            response = self.get()
            response.body = ''
        if response is None:
            self.response.write('')
        return self.response

    def options(self):

        ''' Run GET, clear response, return headers only. '''

        for k, v in self.baseHeaders.items():
            if k.lower() == 'access-control-allow-origin':
                if v == None:
                    self.response.headers[k] = self.request.headers['origin']
            else:
                self.response.headers[k] = v
        return self.response.write(','.join([i for i in frozenset(['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS']) if hasattr(self, i.lower())]))
