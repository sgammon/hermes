# -*- coding: utf-8 -*-

'''
Raw Data API: Exceptions

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# API Exceptions
from api.services import exceptions


## Error - generic top-level exception for all `RawDataService` errors.
class Error(exceptions.Error): ''' Root, abstract `RawDataService` error class. '''
