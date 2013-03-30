# -*- coding: utf-8 -*-

#
# DOCS COMING SOON :)
#

# stdlib / app
import time
import config
import bootstrap

# gevent
import gevent
from gevent import local
from gevent import monkey
from gevent import pywsgi

# momentum/deps
import webob
import apptools
import appfactory

# uWSGI
try:
    import uwsgi
except ImportError as e:
    ## Not running from uWSGI.
    PLATFORM = 'WSGI'
    monkey.patch_all()
else:
    # Monkey-patching is done for us in production by uWSGI
    PLATFORM = 'uWSGI'

# Greenlet locals
_locals = local.local()

# Tracker
from components import tracker

## Spawn server singleton
EventTracker = tracker.EventTracker(PLATFORM)

def devserver():

    ''' Start a local listener for development. '''

    # We're running this from the command line. Start an independent gevent server.
    server = pywsgi.WSGIServer(('', 8080), EventTracker)
    server.serve_forever()
    print "Closed listener."


## Handle full-listener debug spawn
if __name__ == "__main__":
    devserver()
