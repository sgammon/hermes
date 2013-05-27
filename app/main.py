# -*- coding: utf-8 -*-

"""
This is where it all begins... ah, the wonderful *main.py*.
From here, we stitch together :py:mod:`apptools` and :py:mod:`gevent`
to provide an entrypoint for :py:mod:`apptools.dispatch`.

In addition to being the WSGI entrypoint for AppFactory (and any other WSGI-compliant
platform), this is also where you run the devserver...

Running the devserver
---------------------

Only one WSGI application can be run at a time, and running ``Hermes``
can easily be done from the command line.

From the root of your project (the folder outside *app/*):

.. code-block :: console

    $ tools/devserver

    ==== Hermes Devserver ====
    Preloaded module bundle: "apptools".
    Preloaded module bundle: "tracker".
    Failed to preload compiled templates.
    Preloaded module bundle: "hermes".
    [TRACKER]: Datastore: Initialized datastore engine.
    [TRACKER]: Debug mode is ON, serving on port 8080.

    !! Started listener for app <components.tracker.EventTracker> on host/port :8080. !!


If you'd like to start up on port 80 instead:

.. code-block :: console

    $ sudo tools/devserver --port=80


.. note :: For ports under 1024, Unix/Linux requires the use of :command:`sudo`.


Dispatching in production
-------------------------

Many platforms, including *AppFactory* and *Google App Engine*, dispatch Python applications
over WSGI. **This app's main module can be used with WSGI** - applications are exported at
:py:class:`main.EventTracker` and :py:class:`main.APIServer` for *EventTracker* and *Hermes*,
respectively.

Here's a sample *app.yaml* file for *AppFactory*:

.. code-block :: yaml

    appfactory:
      dispatch: main:APIServer
      processes: 2
      threads: 20

As you might imagine, the above will start 2 app processes with 20 dedicated app threads each.
Apps hosted on :py:mod:`gevent` are just as easy:

.. code-block :: yaml

    appfactory:
        dispatch: main:EventTracker
        runtime: gevent
        greenlets: 1000
        processes: 1


Note that *AppFactory* will monkey-patch the CPython standard library for you when you use
the ``gevent`` runtime. To prevent this behavior, simply append ``monkey: off``.

.. note :: Multiple processes with :py:mod:`gevent` enabled is **not recommended**. In many
           cases, you can actually achieve *better* concurrency using Greenlets in a single
           process only, as the native OS management overhead tends to outweigh performance
           benefits significantly.


Just for good measure, here is an *AppEngine*-compatible *app.yaml* file (you can also
specify an *appfactory.yaml* file to avoid compatibility issues and run on *both* platforms!):

.. code-block :: yaml

    application: my-cool-app
    version: docs-sample

    runtime: python27
    api_version: 1
    threadsafe: yes

    handlers:

    - url: /v1
      script: main.APIServer

    - url: /.*
      script: main.EventTracker


To be clear, those module endpoints are completely *WSGI-compliant*, meaning you could
also simply import them and run them however you want, even from a regular Python shell.


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

if 'threading' in sys.modules:
    print Exception('Threading module loaded before patching! Gevent may throw `KeyErrors`.')

# gevent
import gevent
from gevent import local
from gevent import monkey

# uWSGI
try:
    import uwsgi; PLATFORM = 'uWSGI'
except ImportError as e:
    ## Not running from uWSGI.
    PLATFORM = 'WSGI'
    monkey.patch_all()

# PyPy
try:
    import pypycore; RUNTIME = 'PyPy'
except ImportError as e:
    ## Not running in PyPy.
    RUNTIME = 'CPython'

import config
import bootstrap

# prepare sys.path
bootstrapper = bootstrap.AppBootstrapper.prepareImports()

# apptools, by momentum :)
import apptools

# apptools central dispatch
from apptools import dispatch

# pragma: no cover
# (coverage disabled - this is mostly a runfile)

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


def devserver(app, args, port=config._DEVSERVER_PORT, host=config._DEVSERVER_HOST):  # pragma: no cover

    ''' Start a local listener for development, using :py:mod:`gevent.pywsgi`.

        :param app:
            WSGI application to run. Defaults to :py:mod:`apptools.dispatch.gateway`.

        :param port:
            Port to run the application on. Defaults to the value of :py:attr:`config._DEVSERVER_PORT`,
            which is usually set to ``8080``.

        :param host:
            IP to bind the devserver to. Defaults to the value of :py:attr:`config._DEVSERVER_HOST`,
            which is usually set to ``127.0.0.1``. Setting this value to an empty string binds to
            all available IPs - *make sure it is not set to this in production*.

        .. note :: Dispatching this function from Python (or the command line) will block forever
                   via :py:meth:`pyuwsgi.WSGIServer.serve_forever`.

    '''

    global _locals
    global _patched
    global _runcount

    if len(args) and args[0] == '+':
        print os.getpid()
        _OUTPUT = False  # silence all other output
        if len(args) > 1:
            if len(args) > 2:
                _OUTPUT, _TIMEOUT, port = False, args[1], args[2]
            else:
                _OUTPUT, _TIMEOUT = False, args[1]
        else:
            _OUTPUT = False  # allow output and set no timeout
    else:
        _OUTPUT, _TIMEOUT = True, None

    # mock devserver
    from gevent import pywsgi

    if _OUTPUT:
        print "Starting listener for app %s on host/port %s:%s..." % (app, host, port)

    if not _patched:
        # Patch stdlib for gevent
        monkey.patch_all()
        _patched = True

    prefix = os.path.abspath(__file__).split('/')[0:-2]

    if isinstance(app, (type(devserver), type)):
        appname = app.__name__
    else:
        appname = app.__class__.__name__

    if config.debug and sysconfig.get('hooks', {}).get('callgraph', {}).get('enabled', False):  # enable callgraph?

        try:
            import pycallgraph; _CALLGRAPH = True
        except ImportError:
            _CALLGRAPH = False
        else:
            if _OUTPUT:
                print "Callgrapher enabled..."

        if _CALLGRAPH:

            ## define runnable that injects callgrapher
            def callgraphed_application(*args, **kwargs):

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

            application = callgraphed_application

    elif (config.debug and sysconfig.get('hooks', {}).get('profiler', {}).get('enabled', False)):  # enable profiler?

        if _OUTPUT:
            print "Running devserver with profiler enabled..."

        # profiler + inspector
        try:
            import cProfile
            profile = cProfile
        except ImportError:
            import profile

        ## define runnable that injects profiler
        def profiled_application(*args, **kwargs):

            ''' Run application, instrumented with cProfile. '''

            global _runcount

            profiler = profile.Profile()

            # run with profiler, optionally tracing as we go
            for chunk in profiler.runcall(app, *args, **kwargs):
                yield chunk

            _runcount = _runcount + 1
            profiler.dump_stats('/'.join(prefix + ['.profile', '%s-%s.profile' % (appname, _runcount)]))

            if _OUTPUT:
                print "Dumped profiler stats."
            raise StopIteration()

        application = profiled_application

    else:
        application = app  # no shim

    server = pywsgi.WSGIServer((host, port), application)
    if _TIMEOUT:
        try:
            try:
                gevent.with_timeout(float(_TIMEOUT), server.serve_forever)
            except gevent.Timeout:
                server.stop()
                if _OUTPUT:
                    print "Closed listener."
        except KeyError:
            pass
        finally:
            sys.exit(0)

    else:
        server.serve_forever()

    if _OUTPUT:
        print "Closed listener."
    exit(0)


## Handle full-listener debug spawn
if __name__ == "__main__":  # pragma: no cover
    if len(sys.argv) > 1:
        args = sys.argv[1:]
    else:
        args = []
    devserver(APIServer, args)
