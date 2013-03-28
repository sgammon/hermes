# -*- coding: utf-8 -*-

#
# DOCS COMING SOON :)
#

# gevent
import gevent
from gevent import local

# Greenlet locals
_locals = local.local()

# Constants
debug = True  # toggle debug mode
verbose = True  # toggle verbose logging
_BLOCK_PDB = False  # PDB-stop immediately on __call__ - DANGEROUS, DO NOT USE IN PRODUCTION
_API_VERSION = "v1"  # prefix for tracking / API URLs
_PARAM_SEPARATOR = "_"  # seperator between prefix and param name
_REDIS_WRITE_POOL = 50  # perform up to X writes to redis concurrently
_DISCARD_NOSENTINEL = True  # refuse all incoming events missing a sentinel key
_RUNTIME_SOCKROOT = '/ns/runtime/sock'  # root for all unix domain sockets
