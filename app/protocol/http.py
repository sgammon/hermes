# -*- coding: utf-8 -*-

"""
Protocol: HTTP Bindings

Defines HTTP-specific protocol bindings
and ancillary support bindings.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# meta protocol
from . import meta


## DataSlot
# Enumerates available slots for data in the HTTP protocol.
class DataSlot(meta.ProtocolDefinition):

    ''' Maps HTTP data slots to discrete values. '''

    PARAM = 0x1  # POST or GET parameters (webapp2 abstracts this for us. MUST BE == 1).
    ETAG = 0x2  # etag-based tracking (will automatically activate etags if mapped)
    HEADER = 0x3  # request or response headers (mapped to `flags` and `opts` in services)
    COOKIE = 0x4  # HTTP cookie, where key is the name of the cookie
    PATH = 0x5  # HTTP path component (inside the URL)


## RequestMethod
# Indicates the HTTP method of a tracker request.
class RequestMethod(meta.ProtocolDefinition):

    ''' Maps HTTP verbs to discrete values. '''

    GET = 0x1  # HTTP GET - used 99% of the time
    POST = 0x2  # HTTP POST - used for server-side tracker requests
    PUT = 0x3  # HTTP PUT - used for updates/bulk tracker uploads
    DELETE = 0x4  # HTTP DELETE - not used, should yield 400
    HEAD = 0x5  # HTTP HEAD - not used, should yield 400
    OPTIONS = 0x6  # HTTP OPTIONS - used for CORS integration
    TRACE = 0x7  # HTTP TRACE - not used, should yield 400
