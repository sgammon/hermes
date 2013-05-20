# -*- coding: utf-8 -*-

'''
Contains models that express `Tracker` schema, which is a discrete
endpoint for tracking events of a certain profile or type.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.

'''

# stdlib
import time
import datetime

# apptools models
from apptools import model

# hermes models
from api.models.tracker import profile


## Tracker
# Represents a URL that may be hit with tracking events.
class Tracker(model.Model):

    ''' A discrete endpoint for `EventTracker`. '''

    scope = model.Key, {'indexed': True}  # scoped owner of this tracker: can be a client, contract, ad, etc.
    templates = dict, {'indexed': False}  # templates for each event type: CUSTOM _or_ IMPRESSION/CLICK/CONVERSION
    profiles = profile.Profile, {'repeated': True, 'indexed': True}  # profiles linked to this tracker
