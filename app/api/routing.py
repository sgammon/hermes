# -*- utf-8 -*-

'''

API: Routes

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# webapp2
from webapp2 import Route
from webapp2_extras import routes


def get_rules():

	''' Return URL routing rules. '''

	return [

		routes.HandlerPrefixRoute('api.handlers.', [
			Route('/', name='landing', handler='test.TestHandler')
		])

	]
