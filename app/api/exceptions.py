# -*- utf-8 -*-

'''
API: Exceptions

Top-level exceptions are defined here, including Hermes'
package-level catchall, defined as `Error`.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''


## Error - generic top-level exception for all Hermes errors.
class Error(Exception): ''' Root, abstract Hermes error class. '''


## TrackerError - top-level exception for all `EventTracker`-related errors.
class TrackerError(Error): ''' Root, abstract `EventTracker` error class. '''
