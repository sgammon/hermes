# -*- coding: utf-8 -*-

'''
Config: AppFactory

This file holds config for the `appfactory` package, which enables
integration between AppFactory and AppTools.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

"""

    ######################################## layer9/appfactory configuration. ########################################

"""

config = {}

config['layer9.appfactory'] = {

    'enabled': True,
    'logging': False,

    'headers': {
        'full_prefix': 'X-AppFactory',
        'compact_prefix': 'XAF',
        'use_compact': True
    }

}

config['layer9.appfactory.upstream'] = {

    'debug': False,
    'enabled': True,

    'preloading': {
        'gather_assets': False,
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

config['layer9.appfactory.frontline'] = {

    'debug': False,
    'enabled': True

}

config['layer9.appfactory.controller'] = {

    'debug': False,
    'enabled': True

}
