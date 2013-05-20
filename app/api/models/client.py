# -*- coding: utf-8 -*-

'''
This package holds model classes related to Ampush clients,
and modelling relationships between them, contracts, and
ad/aggregation models.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# tracker models
from api.models import TrackerModel


## Client
# Represents a client of Ampush's that holds active contracts.
class Client(TrackerModel):

    ''' Represents an Ampush client with active contracts.

        :param name: String shortname for a client - must be all lowercase and
                     absent of any special symbols, as it will be used in URLs
                     and unique IDs (this is used as the key name for a
                     :py:class:`Client`)

        :param label: Longer, human-readable name for a client. Casing and
                      symbols are allowed, as this value is used in UIs. '''

    name = basestring, {'required': True, 'indexed': True}
    label = basestring, {'required': True, 'indexed': True}


## Contract
# Represents a contract held by an Ampush client.
class Contract(TrackerModel):

    ''' Represents a contract held by an Ampush client.

        :param active: Boolean indicating whether this :py:class:`Contract` is
                       currently active. Defaults to ``False``.

        :param client: Reference :py:class:`apptools.model.Key` to the owner
                       :py:class:`Client` for this :py:class:`Contract`. '''

    active = bool, {'default': False, 'indexed': True}
    client = Client, {'required': True, 'indexed': True}
