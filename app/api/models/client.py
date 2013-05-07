# -*- coding: utf-8 -*-

'''

Models: Client

This package holds model classes related to Ampush clients,
and modelling relationships between them, contracts, and
ad/aggregation models.

-sam (<sam.gammon@ampush.com>)

'''

# tracker models
from api.models import TrackerModel


## Client
# Represents a client of Ampush's that holds active contracts.
class Client(TrackerModel):

	''' Represents an Ampush client with active contracts. '''

	name = basestring, {'required': True, 'indexed': True}
	label = basestring, {'required': True, 'indexed': True}


## Contract
# Represents a contract held by an Ampush client.
class Contract(TrackerModel):

	''' Represents a contract held by an Ampush client. '''

	active = bool, {'default': False, 'indexed': True}
	client = Client, {'required': True, 'indexed': True}
