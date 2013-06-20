# -*- coding: utf-8 -*-

'''

Special Protocol

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# Protocol
from protocol import meta


## Prefixes
# Enumerates special string prefixes for underlying machinery.
class Prefixes(meta.ProtocolDefinition):

    ''' Enumerates special prefixes for keys used
        by `EventTracker` internals to manage
        advanced features like aggregation,
        attribution and integration. '''

    INDEX = '__index__'  # used by apptools internals to index properties by value
    KEY_INDEX = '__key__'  # used by apptools internals to index keys and ancestry
    REVERSE_INDEX = '__reverse__'  # used by apptools internals to resolve forward indexes
    AGGREGATION = '__aggregation__'  # used by ``EventTracker`` to store aggregated property values
    ATTRIBUTION = '__attribution__'  # used by ``EventTracker`` to store attribution adjacency sets


## Separators
# Enumerates special string separators for underlying machinery.
class Separators(meta.ProtocolDefinition):

    ''' Enumerates special string separators that
        are used in underlying data machinery. '''

    PATH = '.'  # separator for property / definition paths
    HASH_CHUNK = '::'  # separator for hash chunks
    HASH_KEY_NAME = '-'  # separator for hash bucket names
    HASH_KEY_VALUE = ':'  # separator for bucket value items
