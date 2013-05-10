# -*- coding: utf-8 -*-

'''

PubSub API: Exceptions

-sam (<sam.gammon@ampush.com>)

'''

# API Exceptions
from api.services import exceptions


## Error - generic top-level exception for all `PubSubService` errors.
class Error(exceptions.Error): ''' Root, abstract `PubSubService` error class. '''
