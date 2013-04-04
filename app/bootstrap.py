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


## AppBootstrapper - does basic app startup/boot tasks.
class AppBootstrapper(object):

	''' Bootstrap this app for WSGI. '''

	injected_paths = 'app', 'app/lib', 'app/lib/dist', '/momentum'

	@classmethod
	def prepareImports(cls):

		''' Prepare Python import path. '''

		for p in cls.injected_paths:
			if p not in sys.path:
				sys.path.append(p)
		return cls
