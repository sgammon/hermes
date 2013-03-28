# - coding: utf-8 -

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
from apps.hermes.source import tools
from apps.hermes.source import debug
from apps.hermes.source import verbose
from apps.hermes.source import exceptions
from apps.hermes.source import _BLOCK_PDB
from apps.hermes.source import _API_VERSION

# components
from apps.hermes.source import components
from apps.hermes.source.components import tracker


## Spawn server singleton
EventTracker = tracker.EventTracker(PLATFORM)

## Handle full-listener debug spawn
if __name__ == "__main__":
    # We're running this from the command line. Start an independent gevent server.
    server = pywsgi.WSGIServer(('', 8080), EventTracker)
    server.serve_forever()
    print "Closed listener."
