# -*- utf-8 -*-

'''
API: Routes

This file contains API routing rules that pass requests
bound to certain URLs to the mapped handler.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# webapp2
from webapp2 import Route
from webapp2_extras import routes


_VERSION_PREFIX = 'v1'


def get_rules():

    ''' Return URL routing rules. '''

    return [

        routes.HandlerPrefixRoute('api.handlers.', [
            Route('/__tracker', name='tracker-root', handler='tracker.TrackerEndpoint'),
            Route('/%s/sandbox' % _VERSION_PREFIX, name='harness-sandbox', handler='harness.Sandbox'),
            Route('/%s/tracker' % _VERSION_PREFIX, name='harness-tracker', handler='harness.Tracker'),
            Route('/%s/sandbox/harness' % _VERSION_PREFIX, name='harness-landing', handler='harness.Landing')
        ])

    ]
