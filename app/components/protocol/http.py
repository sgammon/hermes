# -*- coding: utf-8 -*-

'''
Components: HTTP Protocol

Description coming soon.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Protocol
from . import meta


## ResponseStage - indicates the status of a request/response cycle
class ResponseStage(meta.ProtocolDefinition):

    ''' Maps request stages to discrete values. '''

    PENDING = 0  # pending - the server is processing the request, no response headers yet
    STARTED = 1  # started - response headers have been sent, waiting to yield content
    COMPLETE = 2  # complete - response has been sent, can no longer yield content


## RequestMethod - indicates the HTTP method of a tracker request.
class RequestMethod(meta.ProtocolDefinition):

    ''' Maps HTTP verbs to discrete values. '''

    GET = 0x1  # HTTP GET - used 99% of the time
    POST = 0x2  # HTTP POST - used for server-side tracker requests
    PUT = 0x3  # HTTP PUT - used for updates/bulk tracker uploads
    DELETE = 0x4  # HTTP DELETE - not used, should yield 400
    HEAD = 0x5  # HTTP HEAD - not used, should yield 400
    OPTIONS = 0x6  # HTTP OPTIONS - used for CORS integration
    TRACE = 0x7  # HTTP TRACE - not used, should yield 400
