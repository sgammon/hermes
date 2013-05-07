# -*- coding: utf-8 -*-

'''

App Config

This directory holds all of your apps' configuration info. AppTools can stitch together multiple config
files, as long as they export a `config` dictionary (add config files below in `apptools.system.include`...).

AppTools ships with a few other config files in this folder.

-sam (<sam.gammon@ampush.com>)

'''

import os
import sys
import logging

try:
    import bootstrap

    if 'lib' not in sys.path or 'lib/distlib' not in sys.path:
        bootstrap.AppBootstrapper.prepareImports()

except ImportError as e:
    pass  # we don't care if the bootstrapper can't be found/can't run


## Globals
_config = {}
_compiled_config = None

## Check if we're running on top of the appengine devserver
force_debug = False  # toggle debug mode
strict = False  # toggle strict mode
verbose = True  # toggle verbose logging
production = (os.environ.get('APPFACTORY') == 'production') or (os.environ.get('SERVER_SOFTWARE', 'Not Google').startswith('Google'))
debug = force_debug or (not production)

## App details
appname = 'ampush-hermes'
appversion = '0-3-alpha'


"""

    ######################################## Hermes configuration. ########################################
   

"""


# Constants
verbose = False  # toggle verbose logging
_REDIS_DB = 1  # redis database number
_REDIS_SOCK = 'redis.sock'  # redis socket location
_DEBUG_PORT = 80  # port to bind the gevent pywsgi debug server to
_BLOCK_PDB = False  # PDB-stop immediately on __call__ - DANGEROUS, DO NOT USE IN PRODUCTION
_API_VERSION = "v1"  # prefix for tracking / API URLs
_HEADER_PREFIX = "AMP"  # HTTP header prefix
_DEVSERVER_HOST = ''  # bind to all IP's for dev server
_DEVSERVER_PORT = 80  # port that we should run the devserver on
_PARAM_SEPARATOR = "_"  # seperator between prefix and param name
_REDIS_WRITE_POOL = 200  # perform up to X writes to redis concurrently
_DISCARD_NOSENTINEL = True  # refuse all incoming events missing a sentinel key
_RUNTIME_SOCKROOT = '/ns/runtime/sock'  # root for all unix domain sockets
_PREBUFFER_THRESHOLD = 60  # configurable task limit per prebuffer batch
_PREBUFFER_FREQUENCY = 30  # configurable time threshold for prebuffer flush


"""

    ######################################## Webapp2 configuration. ########################################
   

"""

_config['webapp2'] = {

    'apps_installed': [
        'api'  # Installed projects
    ],

}

_config['webapp2_extras.sessions'] = {

    'secret_key': 'cvxovccvJ)(J@)928)!(*)@(Jiucxohnzoimn0a9MK)(@!)!(@)()CJU09ficu09ei0(!@#)(N)*J)(XJK_()KJ!_)(K',
    'default_backend': 'securecookie',
    'cookie_name':     'amps',
    'session_ttl':     172000000,
    'session_max_age': None,
    'cookie_args': {
        'name':       'aps',
        'max_age':     172000000,
        #'domain':      '*',
        'path':        '/'
        #'secure':      False,
        #'httponly':    False
    },
    'require_valid': True

}

_config['webapp2_extras.jinja2'] = {

    'template_path': 'api/templates/source',  # Root directory for template storage
    'compiled_path': 'api.templates.compiled',  # Compiled templates directory
    'force_compiled': False,  # Force Jinja to use compiled templates, even on the Dev server

    'environment_args': {  # Jinja constructor arguments
        'optimized': True,   # enable jinja2's builtin optimizer (recommended)
        'autoescape': True,  # Global Autoescape. BE CAREFUL WITH THIS.
        'trim_blocks': False,  # Trim trailing \n's from blocks.
        'auto_reload': True,  # Auto-reload templates every time.
        'extensions': ['jinja2.ext.autoescape', 'jinja2.ext.with_', 'jinja2.ext.loopcontrols'],
    }

}


"""

    ######################################## Core configuration. ########################################

    Core system configuration, including settings for the WSGI app, config files, and installed Platforms.

"""

## System Config
_config['apptools'] = {}
_config['apptools.system'] = {

    'debug': False,  # System-level debug messages

    'config': {
        'debug': False  # configuration debug
    },

    'hooks': {  # System-level Developer's Hooks
        'appstats': {'enabled': False},  # AppStats RPC optimization + analysis tool
        'apptrace': {'enabled': False},  # AppTrace memory usage optimization + analysis tool
        'profiler': {'enabled': True}   # Python profiler for CPU cycle/efficiency optimization + analysis
    },

    'include': [  # Extended configuration files to include

        ('layer9', 'config.appfactory'),      # Layer9 Hosting Config
        ('extensions', 'config.extensions'),  # extension config
        ('project', 'config.project'),        # Base Project config
        ('services', 'config.services'),      # Global + site services (RPC/API) config
        ('assets', 'config.assets'),          # Asset manangement layer config
        ('middleware', 'config.middleware'),  # Config for service and handler middleware.

    ]

}

## Platform Config
_config['apptools.system.platform'] = {

    'installed_platforms': [

        {'name': 'Generic WSGI', 'path': 'apptools.platform.generic.GenericWSGI'},
        #{'name': 'Google App Engine', 'path': 'apptools.platform.appengine.GoogleAppEngine'},
        {'name': 'Layer9 AppFactory', 'path': 'apptools.platform.appfactory.AppFactory'},
        #{'name': 'AmpushHermes', 'path': 'api.platform.ampush.hermes'},
        #{'name': 'AmpushFacebook', 'path': 'yoga.platform.tantric.facebook.Facebook'}

    ]

}



"""
###    === Don't modify below this line... ===
"""


def systemLog(message, _type='debug'):

    ''' Logging shortcut. '''

    global debug
    global _config
    if _config['apptools.system']['debug'] is True or _type in ('error', 'critical'):
        prefix = '[CORE_SYSTEM]: '
        if _type == 'debug' or debug is True:
            logging.debug(prefix + message)
        elif _type == 'info':
            logging.info(prefix + message)
        elif _type == 'error':
            logging.error(prefix + message)
        elif _type == 'critical':
            logging.critical(prefix + message)


def readConfig(config=_config):

    ''' Parses extra config files and combines into one global config. '''

    global _compiled_config
    from webapp2 import import_string
    if _compiled_config is not None:
        return _compiled_config
    else:
        if config['apptools.system'].get('include', False) is not False and len(config['apptools.system']['include']) > 0:
            systemLog('Considering system config includes...')
            for name, configpath in config['apptools.system']['include']:
                systemLog('Checking include "' + str(name) + '" at path "' + str(configpath) + '".')
                try:
                    loaded_config = import_string('.'.join(configpath.split('.') + ['config']))
                    config.update(loaded_config)
                except Exception, e:
                    systemLog('Encountered exception of type "' + str(e.__class__) + '" when trying to parse config include "' + str(name) + '" at path "' + str(configpath))
                    if debug:
                        raise
                    else:
                        continue
        if len(config) > 0 and _compiled_config is None:
            _compiled_config = config

        return config

## Export compiled app config
config = readConfig(_config)
