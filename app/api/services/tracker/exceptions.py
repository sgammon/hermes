# -*- coding: utf-8 -*-

'''
Tracker API: Exceptions

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# API Exceptions
from api.services import exceptions


## Error - generic top-level exception for all `TrackerService` errors.
class Error(exceptions.Error): ''' Root, abstract `TrackerService` error class. '''


## TrackerException - abstract parent for all exceptions related to :py:class:`Tracker`.
class TrackerException(Error): pass


## TrackerNotFound - raised when an attempt to retrieve a :py:class:`Tracker` fails because it does not exist.
class TrackerNotFound(TrackerException): ''' Raised when an expected :py:class:`Tracker` does not exist. '''


## ProvisionFailed - raised when an attempt to provision a new tracker fails for some reason.
class ProvisionFailed(TrackerException): ''' Raised when a request to provision a tracker fails. '''
