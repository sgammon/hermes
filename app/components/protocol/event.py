# -*- coding: utf-8 -*-

'''

Components: Event Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# Protocol
from . import meta


## EventType - keeps track of defined event types
class EventType(meta.ProtocolDefinition):

    ''' Keeps track of event types that we track. '''

    IMPRESSION = "i"  # impression - record that an ad was seen.
    CLICK = "c"  # click - record that an ad was clicked on.
    CONVERSION = "v"  # conversion - record that an ad converted a new user.
    CUSTOM = 'x'  # custom - record a custom-defined event type.


## EventProvider - keeps track of event sources
class EventProvider(meta.ProtocolDefinition):

    ''' Keeps track of sources of events we track. '''

    CLIENT = 'cli'  # client - event triggered/provided by the client
    AMAZON = 'amz'  # amazon - event triggered/provided by amazon's systems
    FACEBOOK = 'fb'  # facebook - event triggered/provided by facebook's site/systems
    HASOFFERS = 'hs'  # hasoffers - server-sent event triggered/provided by hasoffers integration
    AD_X = 'adx'  # ad-X - server-sent event triggered/provided by AD-X integration


## EventProperty - keeps track of properties on which events may occur
class EventProperty(meta.ProtocolDefinition):

    ''' Keeps track of web properties on which events may occur. '''

    ONSITE = 'on'  # onsite events - actually on a client's site
    OFFISTE = 'off'  # offsite events - offsite or brick-and-mortar events
    EXTERNAL = 'ext'  # external events - offsite/affiliate site events
    FACEBOOK = 'fb'  # facebook events - events that occur on facebook for desktop
    FACEBOOK_MOBILE = 'fbm'  # facebook mobile events - events that occur on facebook for mobile


## EventTypePriority - keeps track of priority multipliers for event types
class EventTypePriority(meta.ProtocolDefinition):

    ''' Keeps track of mapped priorities for event types. '''

    CONVERSION = 0  # first priority: conversions
    CUSTOM = 1  # second priority: potentially important client events
    CLICK = 1  # third priority: clicks
    IMPRESSION = 3  # fourth priority: impressions
