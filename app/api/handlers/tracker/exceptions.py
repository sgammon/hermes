# -*- coding: utf-8 -*-

'''
Exceptions for the main :py:mod:`handlers.tracker`
package, which handles ``EventTracker`` requests.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.-sam (<sam.gammon@ampush.com>)
'''

from api import exceptions


## TrackerHandlerExceptions - root exception for all `TrackerEndpoint` exceptions.
class TrackerHandlerException(exceptions.TrackerError):

    ''' Root, abstract exception for all :py:class:`TrackerEndpoint`-related
        exceptions. '''


## LegacyHandlerException - root exception for all `LegacyEndpoint` exceptions.
class LegacyHandlerException(TrackerHandlerException):

    ''' Root, abstract exception for all :py:class:`LegacyEndpoint`-related
        exceptions. '''

    pass


## InvalidRefcode - raised upon encountering an invalid legacy ``ref`` code.
class InvalidRefcode(LegacyHandlerException, ValueError):

    ''' Describes a generic state of exception related to the ``ref`` param
        during the regular processing cycle for a legacy hit to
        :py:class:`EventTracker`. '''

    pass


## UnknownRefcode - raised upon encountering an unknown legacy ``ref`` code.
class UnknownRefcode(InvalidRefcode):

    ''' Describes a substate of the exception above, wherein the ``ref``
        param is *specifically* invalid because it failed to be
        resolved. '''

    pass
