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

        ## Debug, development, uptime, etc methods for infrastructure/testing/monitoring use
        'system': {
            'enabled': True,
            'service': 'apptools.services.builtin.SystemService',
            'methods': ['echo', 'hello', 'whoareyou', 'manifest'],

            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        },

        ## Assets API - allows asset sync, AJAX access to asset URLs, and dynamic manifest access
        'assets': {
            'enabled': True,
            'service': 'apptools.services.builtin.AssetsService',
            'methods': ['image_url', 'script_url', 'style_url', 'blob_url', 'manifest', 'generate_upload_url'],

            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        },

        ## Tracker API - allows management and configuration of `EventTracker`.
        'tracker': {
            'enabled': True,
            'service': 'api.services.tracker.service.TrackerService',
            'methods': ['echo'],

            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        },

        ## PubSub API - allows publishing/subscribing to the global eventstream.
        'pubsub': {
            'enabled': False,
            'service': 'api.services.pubsub.service.PubSubService',
            'methods': ['publish', 'subscribe', 'unsubscribe'],
            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        },

        ## Event Data API - allows retrieval of event data or eventseries data.
        'event': {
            'enabled': False,
            'service': 'api.services.event.service.EventDataService',
            'methods': [],
            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        },

        ## Raw Data API - allows retrieval of raw eventstream data.
        'raw': {
            'enabled': False,
            'service': 'api.services.raw.service.RawDataService',
            'methods': [],
            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        }

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

        # Feed-Format Mappers
        {'name': 'RSS', 'enabled': False, 'path': 'apptools.services.mappers.RSSRPCMapper'},
        {'name': 'ATOM', 'enabled': False, 'path': 'apptools.services.mappers.ATOMRPCMapper'},

        # *RPC Mappers
        {'name': 'XMLRPC', 'enabled': False, 'path': 'apptools.services.mappers.XMLRPCMapper'},
        {'name': 'JSONRPC', 'enabled': True, 'path': 'apptools.services.mappers.JSONRPCMapper'},

        # Other Mappers
        {'name': 'Protobuf', 'enabled': False, 'path': 'apptools.services.mappers.ProtobufRPCMapper'},
        {'name': 'URLEncoded', 'enabled': False, 'path': 'apptools.services.mappers.URLEncodedRPCMapper'}

    ],

    'middleware': [

        ('authentication', {

            ## Configuration for authentication middleware

            'enabled': True,
            'debug': True,
            'path': 'apptools.services.middleware.AuthenticationMiddleware',
            'args': {

            }

        }),

        ('monitoring', {

            ## Configuration for monitoring middleware

            'enabled': True,
            'debug': True,
            'path': 'apptools.services.middleware.MonitoringMiddleware',
            'args': {

            }

        }),

        ('authorization', {

            ## Configuration for authorization middleware

            'enabled': True,
            'debug': True,
            'path': 'apptools.services.middleware.AuthorizationMiddleware',
            'args': {

            }

        }),

        ('caching', {

            ## Configuration for caching middleware

            'enabled': True,
            'debug': True,
            'path': 'apptools.services.middleware.CachingMiddleware',
            'args': {

            }

        })

    ],

    ## Configuration profiles that can be assigned to services
    'middleware_config': {

        ## Response + data caching middleware
        'caching': {

            'profiles': {

                ## No caching
                'none': {

                    'localize': False,
                    'default_ttl': None,  # Default Time-to-Live for cached items

                    'activate': {
                        'local': False,    # Local browser-side caching, if supported
                        'request': False,  # Caching of full API responses by hashed API requests
                        'internal': False  # Caching inside the remote service object
                    }

                },


                ## Cache things as they are pulled/used by clients
                'lazy': {

                    'localize': False,
                    'default_ttl': 60,

                    'activate': {
                        'local': False,
                        'request': True,
                        'internal': True
                    },

                },

                ## Cache things as they are used, but set low timeouts to avoid stale data
                'safe': {

                    'localize': False,
                    'default_ttl': 60,

                    'activate': {
                        'local': False,
                        'request': False,
                        'internal': True
                    }

                },

                ## Cache things before they are accessed, predictively, and with long timeouts
                'aggressive': {

                    'localize': False,
                    'default_ttl': 120,

                    'activate': {
                        'local': True,
                        'request': True,
                        'internal': True
                    }

                }

            },

            'default_profile': 'none'  # Default caching profile for APIs that don't specify one

        },

        ## Security and permissions enforcement middleware
        'security': {

            'profiles': {

                ## APIs with no security features
                'none': {

                    'expose': 'all',  # Whether to expose existence of this API to javascript clients

                    ## Client authentication
                    'authentication': {
                        'enabled': False
                    },

                    ## Client authorization
                    'authorization': {
                        'enabled': False
                    }

                },

                ## APIs marked public
                'public': {

                    'expose': 'all',

                    'authentication': {
                        'enabled': False,
                        'mode': None
                    },

                    'authorization': {
                        'enabled': False,
                        'mode': None
                    }

                },

                ## APIs marked private
                'private': {

                    'expose': 'admin',

                    'authentication': {
                        'enabled': False,
                        'mode': None
                    },

                    'authorization': {
                        'enabled': False,
                        'mode': None
                    }

                }

            },

            'default_profile': 'public'

        },

        ## Recording and logging middleware
        'recording': {

            'profiles': {

                'none': {
                    'mode': None
                },

                'minimal': {
                    'mode': None
                },

                'full': {
                    'mode': None
                },

                'debug': {
                    'mode': None
                }

            },

        },

    },

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
