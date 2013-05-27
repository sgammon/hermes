# -*- coding: utf-8 -*-

"""
Config: Services

This file holds configuration and registration for service layer
service classes. It also contains configuration for the service
layer itself.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

"""

    ###################################### Services configuration. ######################################

    Configuration for the AppTools service layer, including a list of installed userland API services.


"""

# stdlib
import hashlib

config = {}

# Project Services
config['apptools.project.services'] = {

    'debug': False,    # Return extra debug info in responses
    'enabled': True,   # Disable API services system wide
    'logging': False,  # Logging for service request handling

    # Module-level (default) config
    'config': {
        'hmac_hash': hashlib.sha1,  # Hash algorithm to use for HMAC signatures
        'url_prefix': '/v1/rpc',  # Prefix for all service invocation URLs
        'secret_key': 'vcxijoOIJ!)@(J)(!@J)(v77G(*&@G!(*H!(*&(@!*CX_A)i-x0ic-',  # Secret key for generating HMAC signings
    },

    # Installed API's
    'services': {
    }  # End services

}  # End services


## Global Services
config['apptools.services'] = {

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
