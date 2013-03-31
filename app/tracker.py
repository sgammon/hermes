# - coding: utf-8 -

## LEGACY TRACKER RUNSCRIPT

# stdlib
import time

# gevent
import gevent
from gevent import pool
from gevent import local
from gevent import queue
from gevent import pywsgi
from gevent import monkey

# momentum libs
import webob
import apptools

# uWSGI / vanilla mode
try:
    import uwsgi

except ImportError as e:
    ## Not running in uWSGI.
    PLATFORM = 'WSGI'
    monkey.patch_all()

else:
    # Monkey-patching is done for us in production by uWSGI
    PLATFORM = 'uWSGI'

# app-level code
from . import tools
from . import debug
from . import verbose
from . import exceptions
from . import _BLOCK_PDB
from . import _API_VERSION

# components
from . import components
from components import tracker


## Spawn server singleton
EventTracker = tracker.EventTracker(PLATFORM)

## Handle full-listener debug spawn
if __name__ == "__main__":
    # We're running this from the command line. Start an independent gevent server.
    server = pywsgi.WSGIServer(('', 8080), EventTracker)
    server.serve_forever()
    print "Closed listener."
