# -*- coding: utf-8 -*-

'''
Handlers for the ``EventTracker`` subsystem. These handlers
deal with hits to ``Tracker`` classes, and produce/yield
``RawEvent`` models.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.-sam (<sam.gammon@ampush.com>)
'''

# WebHandler
from api.handlers import WebHandler


## TrackerEndpoint - handles tracker hits.
class TrackerEndpoint(WebHandler):

    ''' Handles `EventTracker` hits. '''

    def get(self):

        ''' HTTP GET
            :returns: Rendered sample HTML. '''

        return "<html><head><title>cool</title></head><body><b>cool</b></body></html>"
