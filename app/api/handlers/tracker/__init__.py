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

# Root
import config

# Policy
from policy import base

# WebHandler
from api.handlers import WebHandler


# detect redis support
try:
    from redis import client; _REDIS = True
except:
    _REDIS = False


## TrackerEndpoint - handles tracker hits.
class TrackerEndpoint(WebHandler):

    ''' Handles `EventTracker` hits. '''

    _config_path = 'handlers.tracker.TrackerEndpoint'

    def entrypoint(self, explicit=False, legacy=False, policy=base.EventProfile):

        ''' HTTP GET
            :returns: Response to a tracker hit. '''

        try:
            # publish raw event first, propagating globally
            # collapse policy for this event, enforce, and fail-out from critical errors
            raw, tracker, event = self.tracker.policy.enforce(self.request, policy, legacy=legacy)

        except Exception as e:

            # thoroughly log error, re-raise in debug mode
            # exceptions should almost never bubble-up this far
            context = (self.__class__.__name__, e.__class__.__name__, str(e))
            self.logging.error('Encountered unhandled exception in `%s` handler class: %s("%s").' % context)

            if config.debug:
                raise  # re-raise in debug, in production the show must go on

        else:

            # store tracked event, then publish
            result = self.tracker.engine.persist(event, pipeline=True)

            if isinstance(result, tuple):
                key, pipeline = result

            else:
                key, pipeline = result, None

            # underlying storage doesn't support pipelining, publish key
            self.tracker.stream.publish(key, pipeline=pipeline, propagate=True)

            # return everything or nothing according to settings
            if explicit:
                return policy, raw, event
            return ''

    get = post = put = entrypoint
