# -*- utf-8 -*-

#
# DOCS COMING SOON :)
#

# Constants
debug = True  # toggle debug mode
verbose = True  # toggle verbose logging
_REDIS_DB = 1  # redis database number
_REDIS_SOCK = 'redis.sock'  # redis socket location
_DEBUG_PORT = 8080  # port to bind the gevent pywsgi debug server to
_BLOCK_PDB = False  # PDB-stop immediately on __call__ - DANGEROUS, DO NOT USE IN PRODUCTION
_API_VERSION = "v1"  # prefix for tracking / API URLs
_HEADER_PREFIX = "AMP"  # HTTP header prefix
_PARAM_SEPARATOR = "_"  # seperator between prefix and param name
_REDIS_WRITE_POOL = 50  # perform up to X writes to redis concurrently
_DISCARD_NOSENTINEL = True  # refuse all incoming events missing a sentinel key
_RUNTIME_SOCKROOT = '/ns/runtime/sock'  # root for all unix domain sockets
_PREBUFFER_THRESHOLD = 10  # configurable task limit per prebuffer batch
_PREBUFFER_FREQUENCY = 60  # configurable time threshold for prebuffer flush

config = {}
