# -*- coding: utf-8 -*-

'''
Event Data API: Exceptions

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# API Exceptions
from api.services import exceptions


## Error - generic top-level exception for all `EventDataService` errors.
class Error(exceptions.Error): ''' Root, abstract `EventDataService` error class. '''


## TrackerError - generic top-level exception relating to :py:class:`Tracker` endpoints.
class TrackerError(Error): ''' Root, abstract :py:class:`Tracker` exception. '''


## InvalidOwner - raised when an owner string for a :py:class:`Tracker` is invalid.
class InvalidOwner(TrackerError): ''' Raised when an owner string is invalid for some reason. '''


## UnknownOwner - raised when an owner string for a :py:class:`Tracker` is unknown to Hermes.
class UnknownOwner(InvalidOwner): ''' Raised when an owner string is unknown to Hermes. '''
