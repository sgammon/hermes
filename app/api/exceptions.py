# -*- utf-8 -*-

'''

API: Exceptions

Top-level exceptions are defined here, including Hermes'
package-level catchall, defined as `Error`.

-sam (<sam.gammon@ampush.com>)

'''


## Error - generic top-level exception for all Hermes errors.
class Error(Exception): ''' Root, abstract Hermes error class. '''
