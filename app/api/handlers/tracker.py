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

# stdlib
import collections

# WebHandler
from api.handlers import WebHandler


## TrackerEndpoint - handles tracker hits.
class TrackerEndpoint(WebHandler):

    ''' Handles `EventTracker` hits. '''

    def get(self):

        ''' HTTP GET
            :returns: Response to a tracker hit. '''

        # publish raw event first, propagating globally
        raw = self.tracker.event.raw(self.request)
        raw.put()  # save raw event

        # collapse policy for this event, enforce, and fail-out from critical errors
        #with self.tracker.policy.interpret(self.tracker.resolve(raw), raw) as event:

        #    # get ready to grab our execution flow
        #    attributions, aggregations, integrations = [collections.deque() for x in (1, 2, 3)]

        #    # first, store the tracked event (which should start a new pipeline for this request)
        #    self.tracker.engine.persist(event, pipeline=True)

        #    # publish tracked event
        #    self.tracker.stream.publish(event, propagate=True)

        #    for attribution in event.attributions:
        #        # @TODO: generate attribution spec
        #        pass
