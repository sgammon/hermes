# -*- coding: utf-8 -*-

'''

AmpushHermes

-sam (<sam.gammon@ampush.com>)

'''

# stdlib / app
import os
import sys
import config
import bootstrap

# prepare sys.path
bootstrap.AppBootstrapper.prepareImports()

# momentum
import apptools

# uWSGI
try:
    import uwsgi
except ImportError as e:
    ## Not running from uWSGI.
    PLATFORM = 'WSGI'
else:
    # Monkey-patching is done for us in production by uWSGI
    PLATFORM = 'uWSGI'

# PyPy
try:
    import pypycore
except ImportError as e:
    ## Not running in PyPy.
    RUNTIME = 'CPython'
else:  # pragma: no cover
    ## Running in PyPy.
    RUNTIME = 'PyPy'

# Globals
_patched = False
_locals = None
sysconfig = config.config.get('apptools.system')

## Server singletons
_APIServer = None
_EventTracker = None


def APIServer(environ, start_response, dispatch=True):

    ''' Bootstrap and dispatch the Hermes API server. '''

    global _APIServer

    # apptools central dispatch
    from apptools import dispatch

    if not _APIServer:
        # Construct server singleton.
        _APIServer = dispatch.gateway

    if dispatch:
        # Dispatch
        return _APIServer(environ, start_response)
    else:
        # Just construct
        return _APIServer


def RealtimeServer(environ, start_response, dispatch=True):

    ''' Bootstrap and dispatch the Hermes Realtime API Server. '''

    # for now, just delegate to APIServer.
    if config.debug:
        raise NotImplemented('RealtimeServer is not yet implemented.')
    return APIServer(environ, start_response, dispatch)


def EventTracker(environ, start_response, dispatch=True):

    ''' Bootstrap and dispatch the Tracker. '''

    # Globals
    global _locals
    global _patched
    global _EventTracker

    # gevent / tracker
    from gevent import local
    from gevent import monkey
    from components import tracker

    if not _patched:
        # Patch stdlib for gevent
        monkey.patch_all()
        _locals = local.local()
        _patched = True

    if not _EventTracker:
        # Construct server singleton.
        _EventTracker = tracker.EventTracker(PLATFORM)

    if dispatch:
        # WSGI Dispatch
        return _EventTracker(environ, start_response)

    else:
        # Just construct
        return _EventTracker


def devserver(app=EventTracker, port=config._DEVSERVER_PORT, host=config._DEVSERVER_HOST):

    ''' Start a local listener for development. '''

    from gevent import pywsgi

    print "Starting listener for app %s on host/port %s:%s." % (app, host, port)
    server = pywsgi.WSGIServer((host, port), app)

    if config.debug and sysconfig.get('hooks', {}).get('profiler', {}).get('enabled', False):
        import cProfile
        print "Running devserver with profiler enabled..."
        cProfile.runctx('server.serve_forever()', globals(), locals(), filename='/'.join(os.path.abspath(__file__).split('/')[0:-2] + ['.profile', 'EventTracker.profile']))
    else:
        server.serve_forever()
    print "Closed listener."


## Handle full-listener debug spawn
if __name__ == "__main__":

    # Select app and run devserver
    app = EventTracker
    if len(sys.argv) > 1:
        if sys.argv[1] == 'tracker':
            app = EventTracker
        elif sys.argv[1] == 'api':
            app = APIServer

    devserver(app)
