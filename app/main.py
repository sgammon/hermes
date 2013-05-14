# -*- coding: utf-8 -*-
"""
    :author: Sam Gammon (sam.gammon@ampush.com)
    :copyright: (c) 2013 Ampush.
    :license: This is private source code - all rights are reserved. For details about
              embedded licenses and other legalese, see `LICENSE.md`.
"""
__docformat__ = 'restructuredtext en'
__version__ = '0.5'

# stdlib / app
import os
import sys
import config
import bootstrap

# prepare sys.path
bootstrapper = bootstrap.AppBootstrapper.prepareImports()

# apptools, by momentum :)
import apptools

# apptools central dispatch
from apptools import dispatch

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

# gevent
import gevent
from gevent import local
from gevent import monkey

# tracker / hermes components
from components import tracker


# Globals
_DEBUG = True  # DANGER: core debug flag, use with caution
_patched = False  # init flag for monkey patching via gevent
_locals = local.local()  # gevent greenlet local storage
_runcount = 0  # only used in debug: current count of profiler runs
sysconfig = config.config.get('apptools.system')

# Preload
bootstrapper.preload(_DEBUG)

## Server singletons
_APIServer = APIServer = dispatch.gateway
_EventTracker = EventTracker = tracker.EventTracker(PLATFORM)


def RealtimeServer(environ, start_response):

    ''' Bootstrap and dispatch the Hermes Realtime API Server. '''

    # for now, just delegate to APIServer.
    if config.debug or _DEBUG:
        raise NotImplemented('RealtimeServer is not yet implemented.')
    return APIServer(environ, start_response, dispatch)


def devserver(app=EventTracker, port=config._DEVSERVER_PORT, host=config._DEVSERVER_HOST):

    ''' Start a local listener for development. '''

    global _locals
    global _patched
    global _runcount

    # mock devserver
    from gevent import pywsgi

    print "Starting listener for app %s on host/port %s:%s." % (app, host, port)

    if app == EventTracker:
        if not _patched:
            # Patch stdlib for gevent
            monkey.patch_all()
            _patched = True

    root_prefix = prefix = os.path.abspath(__file__).split('/')[0:-2]

    if isinstance(app, (type(devserver), type)):
        appname = app.__name__
    else:
        appname = app.__class__.__name__

    if config.debug and sysconfig.get('hooks', {}).get('callgraph', {}).get('enabled', False):  # enable callgraph?

        try:
            import pycallgraph; _CALLGRAPH = True
        except ImportError as e:
            _CALLGRAPH = False
        else:
            print "Callgrapher enabled..."


        if _CALLGRAPH:
            ## define runnable that injects callgrapher
            def application(*args, **kwargs):

                ''' Start measuring the callgraph and dispatch. '''

                global _runcount

                # start tracing right before dispatch
                pycallgraph.start_trace()
                for chunk in app(*args, **kwargs):
                    yield chunk  # exhaust app generator

                # stop tracing after request is finished
                pycallgraph.stop_trace()
                _runcount = _runcount + 1
                pycallgraph.make_dot_graph('/'.join(prefix + ['.profile', '%s-%s-callgraph.png' % (appname, _runcount)]))
                raise StopIteration()

    elif (config.debug and sysconfig.get('hooks', {}).get('profiler', {}).get('enabled', False)):  # enable profiler?

        print "Running devserver with profiler enabled..."

        # profiler + inspector
        try:
            import cProfile as profile
        except ImportError as e:
            import profile

        ## define runnable that injects profiler
        def application(*args, **kwargs):

            ''' Run application, instrumented with cProfile. '''

            global _runcount

            profiler = profile.Profile()

            # run with profiler, optionally tracing as we go
            for chunk in profiler.runcall(app, *args, **kwargs):
                yield chunk

            _runcount = _runcount + 1
            profiler.dump_stats('/'.join(prefix + ['.profile', '%s-%s.profile' % (appname, _runcount)]))
            print "Dumped profiler stats."
            raise StopIteration()

    else:
        application = app  # no shim

    server = pywsgi.WSGIServer((host, port), application)
    server.serve_forever()

    print "Closed listener."
    exit(0)


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
