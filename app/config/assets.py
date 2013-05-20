# -*- coding: utf-8 -*-

"""
Config: Assets

This file holds config for registered static assets, such that
HREFs to css/JS/arbitrary external assets can be formed by the
AppTools Assets API.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

"""

    ###################################### Asset configuration. ######################################

    ~~~  Description:  ~~~

    In this config file, you can specify registered assets for use in the AppTools Assets API.
    This all corresponds to the directory structure under app/assets. Place your static files in
    app/assets/< js | style | ext >/static, and then register them in the proper section below.

    If you register your scripts, stylesheets, and other stuff here, you can generate URLs to your
    static content directly in the template, handler, service, model or pipeline!

    - Sam Gammon <sam.gammon@ampush.com>


    ~~~ Generating Asset URLs ~~~

    In a template:
        {{ asset.script('jquery', 'core') }}   ## library first, package second (see below for definitions)

    In a handler/pipeline/service/model:
        self.get_script_url('jquery', 'core')  ## generated asset URLs honor output settings (e.g. CDN)


    ~~~ Package Config Structure ~~~

    '<type>': {

        ('<package name>', '<type/subdirectory/path>'): {

            'config': {
                'min': True | False,                    # whether it's possible to serve a minified version of this asset (converts filename to <name>.min.<type>. turn on minified assets in output config to activate)
                'version_mode': '<getvar | filename>',  # whether to add the package's version to the URL as a getvar or as part of the filename
                'bundle': '<your.bundle.js>'            # a name for your bundle, so you can combine assets and serve the optimized version if you want
            },

            'assets': {
                '<asset name>': {'min': True | False, 'version': '<version>'},  # override package `min` value, and specify the package version for cachebusting, when versioning is activated
            }

        }

"""
config = {}


# Installed Assets
config['apptools.project.assets'] = {

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
                'd3': {'min': True, 'version': 'v3'},             # D3: data driven documents, yo
                'jacked': {'min': True, 'version': 'v1'}          # Jacked: animation engine on steroids
            }

        },

        ### AppToolsJS ###
        ('apptools', 'apptools'): {

            'config': {
                'version_mode': 'getvar',
                'bundle': 'apptools.bundle.min.js'
            },

            'assets': {
                'base': {'min': True, 'version': 1.6}  # RPC, events, dev, storage, user, etc (see $.apptools)
            }

        },

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

        },

        # Fonts (svg/eot/woff/ttf)
        ('fonts', 'typography'): {

            'config': {
                'min': False,
                'version_mode': 'getvar'
            },

            'assets': {
                'cabin': {'min': False, 'version': 0.2}  # cabin, webfont
            }

        },

    },


    # Other Assets
    'ext': {
     },

}
