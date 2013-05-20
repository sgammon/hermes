# -*- coding: utf-8 -*-

'''
API Services: Exceptions

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Hermes Exceptions
from api import exceptions


## Error - generic top-level exception for all `APIService` errors.
class Error(exceptions.Error): ''' Root, abstract `APIService` error class. '''
