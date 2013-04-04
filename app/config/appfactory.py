# -*- coding: utf-8 -*-

'''

Config: AppFactory

This file holds config for the `appfactory` package, which enables
integration between AppFactory and AppTools.

-sam (<sam.gammon@ampush.com>)

'''

"""

    ######################################## layer9/appfactory configuration. ########################################

"""

config = {}

config['layer9.appfactory'] = {

	'enabled': True,
	'logging': True,

	'headers': {
		'full_prefix': 'X-AppFactory',
		'compact_prefix': 'XAF',
		'use_compact': True
	}

}

config['layer9.appfactory.upstream'] = {

	'debug': True,
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

	'debug': True,
	'enabled': True

}

config['layer9.appfactory.controller'] = {

	'debug': True,
	'enabled': True

}
