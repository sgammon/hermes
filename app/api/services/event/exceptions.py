# -*- coding: utf-8 -*-

'''

Event Data API: Exceptions

-sam (<sam.gammon@ampush.com>)

'''

# API Exceptions
from api.services import exceptions


## Error - generic top-level exception for all `EventDataService` errors.
class Error(exceptions.Error): ''' Root, abstract `EventDataService` error class. '''
