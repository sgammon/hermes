# -*- coding: utf-8 -*-

'''
Contains models that express `Tracker` schema, which is a discrete
endpoint for tracking events of a certain profile or type.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.

'''

# apptools models
from api.models import TrackerModel


## Tracker - discrete endpoint for recording :py:class:`event.TrackedEvent`s against a given :py:class:`Profile`.
class Tracker(TrackerModel):

    ''' A discrete endpoint for `EventTracker`. Referenced from
        :py:class:`event.TrackedEvent` via a key ID reference
        at :py:attr:`TrackedEvent.tracker`. '''

    profile = basestring, {'indexed': True, 'default': None}  # profile for processing events
    account = basestring, {'indexed': True, 'default': None}  # account ID, if any, attached to this tracker
