# -*- coding: utf-8 -*-

'''

Tracker API: Exceptions

-sam (<sam.gammon@ampush.com>)

'''

# API Exceptions
from api.services import exceptions


## Error - generic top-level exception for all `TrackerService` errors.
class Error(exceptions.Error): ''' Root, abstract `TrackerService` error class. '''
