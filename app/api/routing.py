# -*- utf-8 -*-

#
# DOCS COMING SOON :)
#

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
