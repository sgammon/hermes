# -*- coding: utf-8 -*-

'''

Raw Data API: Exceptions

-sam (<sam.gammon@ampush.com>)

'''

# API Exceptions
from api.services import exceptions


## Error - generic top-level exception for all `RawDataService` errors.
class Error(exceptions.Error): ''' Root, abstract `RawDataService` error class. '''
