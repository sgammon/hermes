# -*- coding: utf-8 -*-
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
                'modernizr': {'min': False, 'version': '2.0.6'},  # Modernizr - browser polyfill + compatibility testing
                'jquery': {'min': True, 'version': '1.9.1'},      # jQuery: Write Less, Do More!
                'jquery.ui': {'min': True, 'version': '1.9.2'},   # jQuery UI: kendo depends on this (shoot me now)
                'underscore': {'min': True, 'version': '1.3.1'},  # Underscore: JavaScript's utility belt
                'd3': {'min': True, 'version': 'v3'},             # D3: data driven documents, yo
                'nvd3': {'min': True, 'version': 'v1'},           # NVD3: Pre-packaged D3 routines
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

        ### jQuery Plugins ###
        ('jquery', 'core/jquery'): {

            'config': {
                'version_mode': 'getvar',
                'bundle': 'jquery.bundle.min.js',
                'min': True
            },

            'assets': {
                ## jquery core is included in "core" (see above)
                'easing': {'path': 'interaction/easing.min.js'},          # Easing transitions for smoother animations
                'mousewheel': {'path': 'interaction/mousewheel.min.js'}   # jQuery plugin for mousewheel events + interactions
            }

        },

        ## KendoUI ##
        ('kendo', 'kendo'): {

            'config': {
                'version_mode': 'getvar',
                'bundle': 'kendo.bundle.min.js',
                'min': True
            },

            'assets': {
                'all': {'min': True, 'version': 0.3},
                'fx': {'min': True, 'version': 0.4},
                'core': {'min': True, 'version': 0.4},
                'data': {'min': True, 'version': 0.4},
                'grid': {'min': True, 'version': 0.4},
                'pager': {'min': True, 'version': 0.4},
                'dataviz': {'min': True, 'version': 0.4},
                'mobile': {'min': True, 'version': 0.4}
            }

        },

        ## Zurb Foundataion ##
        ('zurb', 'foundation'): {

            'config': {
                'version_mode': 'getvar',
                'bundle': 'zurb.bundle.min.js',
                'min': True
            },

            'assets': {
                'core': {'min': True, 'version': 0.3}  # zurb foundation
            }

        },

        ### Yoga Platform ###
        ('yoga', 'platform'): {

            'config': {
                'version_mode': 'getvar',
                'bundle': 'platform.bundle.min.js'
            },

            'assets': {
                'tantric': {'min': True, 'version': 1.7}
            }

        },

        ## Tantric Modules ##
        ('tantric', 'platform/tantric'): {
            'config': {
                'version_mode': 'getvar',
                'min': True,
                'bundle': 'tantric.bundle.min.js'
            },
            'assets': {
                'manage': {'min': True, 'version': 1.5},
                'mobile': {'min': True, 'version': 1.5}
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
                'main': {'version': 0.9},  # reset, main, layout, forms
                'security': {'version': 0.6},  # login / security styles
                'mobile': {'version': 0.8},  # mobile styles + responsive
                'print': {'version': 0.6},  # print-friendly styles
                'ie': {'version': 0.6}  # fixes for internet explorer
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

        # Content-section specific stylesheets
        ('site', 'compiled/site'): {

            'config': {
                'min': False,
                'version_mode': 'getvar'
            },

            'assets': {
            }

        },

        # Kendo-specific stylesheets
        ('kendo', 'embedded/kendo'): {

            'config': {
                'min': True,
                'version_mode': 'getvar'
            },

            'assets': {
                'mobile': {'min': True, 'version': 0.3},
                'combined': {'min': True, 'version': 0.3}
            }

        },

        # NVD3-specific stylesheets
        ('nvd3', 'embedded/nvd3'): {

            'config': {
                'min': True,
                'version_mode': 'getvar'
            },

            'assets': {
                'v1': {'min': True, 'version': 1.3}
            }

        },

        # Dashboard Stylesheets
        ('manage', 'compiled/manage'): {

            'config': {
                'min': False,
                'version_mode': 'getvar'
            },

            'assets': {
                'main': {'min': False, 'version': 0.5}
            }

        },

        # App-Specific Stylesheets
        ('gatsby', 'compiled/app/gatsby'): {

            'config': {
                'min': False,
                'version_mode': 'getvar'
            },

            'assets': {
                'main': {'min': False, 'version': 0.4},  # main styles for the great gatsby
                'mobile': {'min': False, 'version': 0.6},  # mobile styles for the great gatsby
                'fonts': {'min': False, 'version': 0.4}  # zocial / gatsby-specific fonts
            }

        }

    },


    # Other Assets
    'ext': {
     },

}
