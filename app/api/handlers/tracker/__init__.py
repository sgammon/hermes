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

# Policy Base
from policy import base
from policy import click
from policy import impression
from policy import conversion


## TrackerEndpoint - handles tracker hits.
class TrackerEndpoint(WebHandler):

    ''' Handles `EventTracker` hits. '''

    def get(self, explicit=False, legacy=False, policy=base.EventProfile):

        ''' HTTP GET
            :returns: Response to a tracker hit. '''

        # publish raw event first, propagating globally
        # collapse policy for this event, enforce, and fail-out from critical errors
        raw, tracker, event = self.tracker.policy.enforce(self.request, policy, legacy=legacy)

        # store tracked event, then publish
        self.tracker.stream.publish(self.tracker.engine.persist(event, pipeline=True), propagate=True)

        # return everything or nothing according to settings
        if explicit:
            return policy, raw, event
        return ''
