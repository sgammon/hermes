# -*- coding: utf-8 -*-

'''

AmpushHermes: Bootstrapper

This small utility file is loaded by AppTools and executed as early
as possible in the execution flow, to facilitate the injection of
paths onto `sys.path`, preloading, and other process-level init for
the app.

-sam (<sam.gammon@ampush.com>)

'''

# stdlib
import os
import sys

# Globals
_bootstrapped = False


## AppBootstrapper - does basic app startup/boot tasks.
class AppBootstrapper(object):

    ''' Bootstrap this app for WSGI. '''

    injected_paths = 'lib', 'lib/dist', '/momentum'

    @classmethod
    def prepareImports(cls):

        ''' Prepare Python import path. '''

        global _bootstrapped

        if not _bootstrapped:
            for p in cls.injected_paths:
                if p not in sys.path:
                    sys.path.append(p)
            _bootstrapped = True
        return cls

AppBootstrapper.prepareImports()
