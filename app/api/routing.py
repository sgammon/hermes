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
            Route('/%s/sandbox' % _VERSION_PREFIX, name='harness-sandbox', handler='harness.SandboxHandler'),
            Route('/%s/sandbox/harness' % _VERSION_PREFIX, name='harness-landing', handler='harness.Landing')
        ])

    ]
