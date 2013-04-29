# -*- coding: utf-8 -*-

'''

API Services: Exceptions

-sam (<sam.gammon@ampush.com>)

'''

# Hermes Exceptions
from api import exceptions


## Error - generic top-level exception for all `APIService` errors.
class Error(exceptions.Error): ''' Root, abstract `APIService` error class. '''
