# -*- coding: utf-8 -*-

'''
App Config

This directory holds all of your apps' configuration info. AppTools can stitch together multiple config
files, as long as they export a `config` dictionary (add config files below in `apptools.system.include`...).

AppTools ships with a few other config files in this folder.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

import os
import hashlib
import logging

## Globals
_config = {}
_compiled_config = None

## Check if we're running on top of the appengine devserver
force_debug = True  # toggle debug mode
strict = False  # toggle strict mode
verbose = True  # toggle verbose logging
_appenv = os.environ.get('APPFACTORY', 'Not Production')  # appfactory role env
_appsft = os.environ.get('SERVER_SOFTWARE', 'Not Google')  # server software env
production = (_appenv == 'production') or (_appsft.startswith('Google'))
debug = force_debug or (not production)

## App details
appname = 'ampush-hermes'
appversion = '0-5-alpha'


"""

    ######################################## Hermes configuration. ########################################


"""


## App settings
_config['apptools.project'] = {

    'name': 'Hermes',            # Change this to your app's name

    'version': {               # Change this according to your app's version
        'major': 0,
        'minor': 5,
        'micro': 0,
        'build': 20130520,
        'release': 'ALPHA'
    }

}

# Constants
verbose = True  # toggle verbose logging
_API_VERSION = "v1"  # prefix for tracking / API URLs
_HEADER_PREFIX = "AMP"  # HTTP header prefix
_DEVSERVER_HOST = ''  # bind to all IP's for dev server
_DEVSERVER_PORT = 8080  # port that we should run the devserver on
_PARAM_SEPARATOR = ""  # seperator between prefix and param name
_REDIS_WRITE_POOL = 200  # perform up to X writes to redis concurrently
_DISCARD_NOSENTINEL = True  # refuse all incoming events missing a sentinel key
_PREBUFFER_THRESHOLD = 60  # configurable task limit per prebuffer batch
_PREBUFFER_FREQUENCY = 30  # configurable time threshold for prebuffer flush


# Redis Adapter
_config['apptools.model.adapters.redis.Redis'] = {

    'debug': False,  # debug messages

    'servers': {

        'default': 'tracker',

        # Redis Instances
        'hermes': {'unix_socket_path': '/ns/runtime/sock/redis.sock', 'db': 0},
        'tracker': {'unix_socket_path': '/ns/runtime/sock/redis.sock', 'db': 1}

    }

}

# Memcache Adapter
_config['apptools.model.adapters.memcache.Memcache'] = {

    'debug': True,  # debug messages

    'servers': {
        'local': {'host': '127.0.0.1', 'port': 11211, 'unix': '/ns/runtime/sock/memcache.sock'}
    }

}

## Output layer settings
_config['apptools.project.output'] = {

    # Output Configuration

    'debug': False,
    'minify': False,       # whether to minify page output or not
    'optimize': True,     # whether to use the async script loader or not
    'standalone': False,  # whether to render only the current template, or the whole context (ignores "extends")

    'analytics': {  # Analytics Settings
        'enable': False,              # whether to insert analytics code
        'multitrack': True,          # whether to enable support for multiple trackers
        'anonymize': False,          # whether to anonymize IPs before analytics
        'account_id': {
            'hermes': 'UA-37219177-3'   # main yoga analytics tracking
        },
        'sitespeed': {
            'enable': True,           # enable google analytics' site speed tracking
            'sample': 100            # set the sitespeed sample rate
        },
        'webclient': {
            'dev': 'https://ssl.google-analytics.com/u/analytics_debug.js',
            'http': 'https://ssl.google-analytics.com/u/analytics_debug.js',
            'https': 'https://ssl.google-analytics.com/u/analytics_debug.js'
        }
    },

    'appcache': {  # HTML5 appcaching
        'enable': False,                       # whether to enable
        'manifest': 'scaffolding-v1.appcache'  # manifest to link to
    },

    'assets': {  # Asset API
        'minified': False,       # whether to switch to minified assets or not
        'serving_mode': 'local',  # 'local' or 'cdn' (CDN prefixes all assets with an absolute URL)
        'cdn_prefix': ['deliver.ampushyoga.io']
        # ^^ CDN prefix/prefixes - a string is used globally, a list of hostnames is selected from randomly for each
    },

    'headers': {  # Default Headers (only supported headers are shown)
        'Vary': 'Content-Encoding',
        'Content-Language': 'en-US,en',
        'Cache-Control': 'private,max-age=3600',  # default to not caching dynamic content
        'X-Powered-By': 'Tracker/v1',
        'X-UA-Compatible': 'IE=edge,chrome=1',  # http://code.google.com/chrome/chromeframe/
        'XAF-Origin': 'AppHosting/Hermes/1.0',

        ## /*****/ CORS /*****/ ##
        'Access-Control-Allow-Origin': None,

        'Access-Control-Allow-Methods': 'GET, POST',

        'Access-Control-Allow-Headers': ','.join([
            'Content-Type', 'Content-Length', 'XAF-Session', 'XAF-Token', 'XAF-Channel',
            'XAF-Socket', 'X-ServiceTransport', 'X-ServiceClient']),

        'Access-Control-Expose-Headers': ','.join([
            'Content-Type', 'Content-Length', 'XAF-Session', 'XAF-Token', 'XAF-Channel',
            'XAF-Socket', 'X-ServiceTransport', 'X-ServiceClient'])
    }

}

_config['apptools.output.meta'] = {

    'icon': '<invalid>',
    'logo': '<invalid>',
    'author': 'Ampush, Inc.',
    'publisher': 'Ampush, Inc.',
    'copyright': 'Ampush, (c) 2013',
    'robots': 'noindex,nofollow',  # 'index,follow',
    'revisit': '7 days',

    'description': 'Hermes test harness and toolchain.',

    'application-name': 'ampush hermes',
    'viewport': 'width=device-width,initial-scale=1,user-scalable=yes,height=device-height',
    'revisit-after': '7 days',

    'keywords': [
        'hermes',
        'api',
        'tools',
        'ampush',
        'json'
    ],

    'opengraph': {

        'title': 'ampush hermes: welcome',
        'type': 'website',
        'determiner': 'a',
        'locale': 'en_US',
        'url': 'https://tools.amp.sh',
        'site_name': 'project hermes',
        'description': 'Hermes test harness and toolchain.',
        'image': '',

        'location': {
            'enable': True,

            'latitude': '',
            'longitude': '',
            'address': '450 9th Street, 2nd Floor',
            'locality': 'San Francisco',
            'region': 'California',
            'zipcode': '94103',
            'country': 'United States of America',
            'email': 'hermes@ampush.com',
            'phone': ''
        },

        'facebook': {
            'app_id': '',
            'admins': ['642005650']
        }

    },

    'apple': {

        'touch_icon': '',
        'precomposed': '',
        'startup_icon': '',
        'status_bar_style': '',
        'app_capable': ''

    },

    'google': {

        'site_verification': ''

    }

}


"""

    ######################################## Service configuration. ########################################


"""


# Project Services
_config['apptools.project.services'] = {

    'debug': False,    # Return extra debug info in responses
    'enabled': True,   # Disable API services system wide
    'logging': False,  # Logging for service request handling

    # Module-level (default) config
    'config': {
        'hmac_hash': hashlib.sha1,  # Hash algorithm to use for HMAC signatures
        'url_prefix': '/v1/rpc',  # Prefix for all service invocation URLs
        'secret_key': 'vcxijoOIJ!)@(J)(!@J)(v77G(*&@G!(*H!(*&(@!*CX_A)i-x0ic-',  # Secret for generating HMAC signings
    },

    # Installed API's
    'services': {
    }  # End services

}  # End services


## Global Services
_config['apptools.services'] = {

    'logging': True,

    'hooks': {
        'appstats': {'enabled': False},  # RPC profiling
        'apptrace': {'enabled': False},  # memory usage profiling
        'profiler': {'enabled': False}   # CPU usage profiling
    },

    'mappers': [
    ],

    'middleware': [],

    ## Configuration profiles that can be assigned to services
    'middleware_config': {},

    ### Default config values
    'defaults': {

        'module': {},
        'service': {

            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            },

            'args': {

            }

        }

    },

}


"""

    ######################################## Webapp2 configuration. ########################################


"""

_config['webapp2'] = {

    'apps_installed': [
        'api'  # Installed projects
    ],

}

_config['webapp2_extras.sessions'] = {

    'secret_key': 'cvnnlkNIOPJM)@!()@(J)(CJ)(JcxnvocinvOPIPOWMWinbiuvb09*H@!)*H)@!(J0c8x70zx8jc',
    'default_backend': 'securecookie',
    'cookie_name': 'amps',
    'session_ttl': 172000000,
    'session_max_age': None,
    'cookie_args': {
        'name': 'hermes',
        'max_age': 172000000,
        #'domain':      '*',
        'path': '/'
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
        'callgraph': {'enabled': False},  # Use `pycallgraph` to generate an image callgraph of the WSGI app
        'profiler': {'enabled': False}   # Python profiler for CPU cycle/efficiency optimization + analysis
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
        {'name': 'Layer9 AppFactory', 'path': 'apptools.platform.appfactory.AppFactory'},
        {'name': 'AmpushHermes', 'path': 'api.platform.hermes.Hermes'},
        {'name': 'EventTracker', 'path': 'api.platform.tracker.Tracker'}

    ]

}


"""

    ######################################## Asset configuration. ########################################

    Configures static assets for use with the Assets API.

"""

# Installed Assets
_config['apptools.project.assets'] = {

    'debug': False,    # Output log messages about what's going on.
    'verbose': False,  # Raise debug-level messages to 'info'.

    # JavaScript Libraries & Includes
    'js': {


        ### Core Dependencies ###
        ('core', 'core'): {

            'config': {
                'version_mode': 'getvar',
                'bundle': 'core.bundle.min.js'
            },

            'assets': {
                'd3': {'min': True, 'version': 'v3'},      # D3: data driven documents, yo
                'jacked': {'min': True, 'version': 'v1'},  # Jacked: animation engine on steroids
                'base': {'min': True, 'version': 1.6}      # RPC, events, dev, storage, user, etc (see $.apptools)
            }

        }

    },


    # Cascading Style Sheets
    'style': {

        # Compiled (SASS) FCM Stylesheets
        ('compiled', 'compiled'): {

            'config': {
                'min': False,
                'version_mode': 'getvar'
            },

            'assets': {
                'main': {'version': 0.9}  # reset, main, layout, forms
            }

        }

    },


    # Other Assets
    'ext': {},

}


"""

    ######################################## layer9/appfactory configuration. ########################################

"""

_config['layer9.appfactory'] = {

    'enabled': True,
    'logging': False,

    'headers': {
        'full_prefix': 'X-AppFactory',
        'compact_prefix': 'XAF',
        'use_compact': True
    }

}

_config['layer9.appfactory.upstream'] = {

    'debug': False,
    'enabled': True,

    'preloading': {
        'gather_assets': True,
        'enable_spdy_push': False,
        'enable_link_fallback': False
    },

    'spdy': {

        'push': {

            'assets': {
                'force_priority': False,
                'default_priority': 7
            }

        }

    }

}

_config['layer9.appfactory.frontline'] = {'debug': False, 'enabled': True}
_config['layer9.appfactory.controller'] = {'debug': False, 'enabled': False}



"""

    ######################################## output extension configuration. ########################################

"""

## DynamicContent extension - manages injection of dynamic, editable content into template AST's
_config['apptools.output.extension.DynamicContent'] = {'enabled': False}

## FragmentCache extension - makes caching possible in the template via a {% cache %} tag
_config['apptools.output.extension.FragmentCache'] = {

    'debug': True,
    'enabled': True,
    'logging': False,

    'config': {
        'timeout': 1200,  # default timeout of 5 minutes
        'prefix': '::'.join(['amp', 'tpl', 'source', 'fragment'])
    }

}

## ThreadedBytecodeCache extension - caches compiled template bytecode in thread memory
_config['apptools.output.extension.ThreadedBytecodeCache'] = {'enabled': False}

## MemcachedBytecodeCache extension - caches compiled template bytecode in memcache
_config['apptools.output.extension.MemcachedBytecodeCache'] = {'enabled': False}


_config['apptools.project.output.template_loader'] = {

    # Template Loader Config

    'force': True,              # Force enable template loader even on Dev server
    'debug': False,             # Enable dev logging
    'use_memory_cache': False,  # Use handler in-memory cache for template source
    'use_memcache': False,      # Use Memcache API for template source

}

# Models/Storage Configuration
_config['apptools.model'] = {

    'debug': False,  # log messages
    'default': 'Memory',  # default storage engine

    'engines': [

        {'name': 'Redis', 'enabled': True, 'path': 'apptools.model.adapter.redis.Redis'},
        {'name': 'Memory', 'enabled': True, 'path': 'apptools.model.adapter.inmemory.InMemory'},
        {'name': 'Memcache', 'enabled': True, 'path': 'apptools.model.adapter.memcache.Memcache'}

    ]

}

_config['apptools.classes.WebHandler'] = {

    'debug': False,
    'logging': True,
    'extensions': {
        'load': ['FragmentCache', 'DynamicContent', 'MemcachedBytecodeCache']
    }

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

config = _config
