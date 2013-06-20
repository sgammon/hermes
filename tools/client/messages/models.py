import datetime
from apptools import model


class TrackerModel(model.Model):

    modified = datetime.datetime, {'auto_now': True, 'indexed': True}
    created = datetime.datetime, {'auto_now_add': True, 'indexed': True}


class Tracker(TrackerModel):

    owner = basestring, {'indexed': True, 'required': True}
    profile = basestring, {'indexed': True, 'default': None}


class TrackedEvent(TrackerModel):

    raw = basestring, {'required': True, 'indexed': False}
    params = dict, {'required': True, 'default': {}, 'indexed': False}
    error = bool, {'required': False, 'indexed': True}
    tracker = basestring, {'required': False, 'indexed': True}
    profile = basestring, {'required': True, 'indexed': True}
    errors = basestring, {'repeated': True, 'indexed': False}
    warnings = basestring, {'repeated': True, 'indexed': False}
    integrations = basestring, {'repeated': True, 'indexed': False}
    aggregations = basestring, {'repeated': True, 'indexed': False}
    attributions = basestring, {'repeated': True, 'indexed': False}


class Event(TrackerModel):

    url = basestring, {'required': True, 'indexed': False}
    method = basestring, {'required': True, 'indexed': False}
    policy = basestring, {'required': False, 'indexed': True}
    timestamp = datetime.datetime, {'required': True, 'indexed': True}
    session = bool, {'required': False, 'indexed': False}
    cookie = basestring, {'indexed': True, 'indexed': False}
    error = bool, {'indexed': True, 'default': False}
    legacy = bool, {'indexed': True, 'default': False}
    processed = bool, {'indexed': False, 'default': False}


class Error(TrackerModel):

    code = basestring
    event = basestring, {'indexed': True}
    message = basestring
    handled = bool, {'default': False}


Tracker = Tracker.to_message_model()
TrackedEvent = TrackedEvent.to_message_model()
Event = Event.to_message_model()
Error = Error.to_message_model()
