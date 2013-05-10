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


_VERSION_PREFIX = 'v1'


def get_rules():

    ''' Return URL routing rules. '''

    return [

        routes.HandlerPrefixRoute('api.handlers.', [
            Route('/%s/test' % _VERSION_PREFIX, name='landing', handler='test.TestHandler'),
            Route('/%s/test/<mode>' % _VERSION_PREFIX, name='landing-mode', handler='test.TestHandler'),
            Route('/%s/sandbox' % _VERSION_PREFIX, name='harness-sandbox', handler='harness.SandboxHandler')
        ])

    ]
