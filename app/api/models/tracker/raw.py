# -*- coding: utf-8 -*-

'''

Tracker Models: Raw

These models are used to express raw tracker events, before they are processed
into full `TrackedEvent` entities.

-sam (<sam.gammon@ampush.com>)

'''

# stdlib
import time
import datetime

# apptools models
from apptools import model


## RawEvent
# Represents a raw hit to a tracker URL.
class RawEvent(model.Model):

    ''' Raw record of a `TrackedEvent`. '''

    id = basestring, {'required': True, 'indexed': False}  # unique request ID from routing infrastructure
    url = basestring, {'required': True, 'indexed': False}  # full text of URL hit (including params + hash, if any)
    session = bool, {'default': False, 'indexed': True}  # whether the request came in with a session (True) or one was created (False)
    processed = bool, {'default': False, 'indexed': True}  # whether this `RawEvent` has been processed into a `TrackedEvent` yet
    cookie = basestring, {'indexed': True, 'indexed': True}  # plaintext value of the cookie in this event
    modified = datetime.datetime, {'required': True, 'auto_now': True}  # timestamp for when this record was last modified
    timestamp = datetime.datetime, {'required': True, 'auto_now_add': True}  # timestamp for when this record was created
