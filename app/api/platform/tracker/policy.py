# -*- coding: utf-8 -*-

'''
The :py:class:`PolicyEngine` class handles the application and
enforcement of event policies. Execution flow for extracting
parameters, generating followup tasks, and aggregation /
attribution happens here.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Platform Parent
from api.platform import PlatformBridge


## PolicyEngine - handles application and enforcement of schema policy.
class PolicyEngine(PlatformBridge):

    ''' Receives resultant/collapsed/materialized policy from
        :py:class:`platform.ampush.tracker.event.EventBuilder`,
        and manages execution flow for applying that policy. '''

    def build(self, policies):

        ''' Compile multiple :py:class:`model.profile.Profile`
            classes into a single, compound policy class.

            :param policies:
            :returns: '''

        pass

    def gather(self):

        ''' Walk the class inheritance chain and gather applicable
            :py:class:`model.profile.Profile` classes, for construction
            into a compound policy for handling an event.

            :param tracker:
            :param context:
            :returns: '''

        pass

    def enforce(self):

        ''' Given a materialized :py:class:`model.event.TrackedEvent`,
            enforce policy decisions, potentially raising exceptions
            encountered along the way.

            :param suite:
            :param strict:
            :returns: Boolean indicating whether the compound policy
                      was found to be valid. '''

        pass

    def interpret(tracker, raw_event):

        ''' Gather, build, enforce and map policy for the
            given :py:class:`model.tracker.Tracker` and
            :py:class:`model.raw.Event`.

            :param tracker:
            :param raw_event:
            :returns: A newly-inflated and provably-valid
                      :py:class:`model.event.TrackedEvent` '''

        pass
