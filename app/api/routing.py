# -*- utf-8 -*-

'''

API: Routes

This file contains API routing rules that pass requests
bound to certain URLs to the mapped handler.

-sam (<sam.gammon@ampush.com>)

'''

# webapp2
from webapp2 import Route
from webapp2_extras import routes


def get_rules():

	''' Return URL routing rules. '''

	return [

		routes.HandlerPrefixRoute('api.handlers.', [
			Route('/v1/test', name='landing', handler='test.TestHandler'),
			Route('/v1/test/<mode>', name='landing-mode', handler='test.TestHandler')
		])

	]
