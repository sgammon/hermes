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

# Policy Base
from policy import *
from policy import base
from policy import core
from policy import click
from policy import impression
from policy import conversion

# Tracker Endpoint
from api.handlers.tracker import exceptions
from api.handlers.tracker import TrackerEndpoint


## LegacyEndpoint - handles legacy tracker hits.
class LegacyEndpoint(TrackerEndpoint):

    ''' Handles `LegacyEndpoint` hits. '''

    def delegate(self, *args, **kwargs):

        ''' Delegate to ``TrackedEndpoint``.
            :returns: Response from :py:class:`TrackerEndpoint`. '''

        return super(LegacyEndpoint, self).get(*args, **kwargs)

    def resolve(self, ref):

        ''' Resolve an appropriate profile for
            the referenced item at ``ref``.

            :param ref: String reference code to match.
            :raises ValueError: In the case of an invalid ``ref``.
            :raises InvalidTracker: In the case of an unknown ``ref``.
            :returns: Matched profile for the given ``ref``. '''

        # force-fail number-like stuff
        for i in (float, int):
            try:
                i(ref)
            except ValueError:
                continue
            else:
                raise exceptions.InvalidRefcode('Received number-like object as `ref`: "%s".' % str(ref))

        # otherwise, match against legacy "ref" names
        for id, profile in core.Profile.registry.iteritems():

            if hasattr(profile, 'refcode'):

                # if the refcode matches, it's what we wanted
                if ref == profile.refcode:
                    return profile

        raise exceptions.UnknownRefcode('Failed to resolve tracker by refcode: "%s".' % ref)

    def get(self, explicit=False):

        ''' HTTP GET
            :returns: Response to a legacy tracker hit. '''

        # modern URLs should never come through here, and all legacy URLs should have ``ref``
        if 'ix' in self.request.params or 'ref' not in self.request.params:
            if 'ix' in self.request.params:
                self.logging.error('Got legacy tracker hit without REF: "%s".' % str(self.request))
            else:
                self.logging.error('Got modern tracker hit to legacy endpoint: "%s".' % str(self.request))
            return self.delegate(explicit=explicit, legacy=False)

        # publish raw event first, propagating globally
        profile = self.resolve(self.request.params.get('ref'))

        return self.delegate(explicit=explicit, legacy=True, policy=profile)
