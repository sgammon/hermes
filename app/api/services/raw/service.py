# -*- coding: utf-8 -*-

'''
Raw Data API: Service

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Local Imports
from . import messages
from . import exceptions

# apptools services
from apptools import rpc
from apptools import model

# Raw Models
from api.models.tracker import raw


## RawDataService - exposes methods for retrieving raw data from `EventTracker`.
@rpc.service
class RawDataService(rpc.Service):

    ''' Exposes methods for retrieving raw data from `EventTracker`. '''

    name = 'raw'
    _config_path = 'hermes.api.tracker.RawDataAPI'

    exceptions = rpc.Exceptions(**{
        'generic': exceptions.Error,
        'invalid_key': exceptions.InvalidKey,
        'not_found': exceptions.NotFound
    })

    @rpc.method(model.Key, raw.Event)
    def get(self, request):

        ''' Retrieve a :py:class:`raw.Event` by its associated
            :py:class:`model.Key`. '''

        try:

            # decode key first
            if request.encoded:
                key = model.Key.from_urlsafe(request.encoded)

            elif request.id:
                key = model.Key(raw.Event, request.id)

            if not key:
                raise self.exceptions.invalid_key('Must provide either a URLsafe-encoded '
                                                  '`model.Key` or valid `model.Key` ID.')

            # pull event
            raw_ev = raw.Event.get(key)

            # fail if we can't find it
            if raw_ev is None:
                raise self.exceptions.not_found('No raw event found at key: "%s".' % raw_ev.urlsafe())

            # otherwise, return
            return raw_ev

        except self.exceptions.generic as e:

            self.logging.error('Encountered bound service exception %s: %s.' % (e.__class__.__name__, str(e)))
            raise  # locally-bound exceptions can be re-raised safely

        except Exception as e:

            context = (e.__class__.__name__, str(e))
            self.logging.error('Encountered unhandled, unbound exception: (%s, %s).' % context)
            raise self.exceptions.generic('Encountered unhandled exception "%s": %s.' % context)

    @rpc.method(messages.RawKeys, messages.RawEvents)
    def get_multi(self, request):

        ''' Retrieve multiple :py:class:`raw.Event` entities
            in batch. '''

        try:

            # decode target keys
            target_keys = []
            for key in request.keys:
                if key.encoded:
                    target_keys.append(model.Key.from_urlsafe(request.encoded))

                elif request.id:
                    target_keys.append(model.Key(raw.Event, request.id))

            # check target keys
            if not all(target_keys):
                for i, key in enumerate(target_keys):  # let user know which was a failure
                    if not key or not key.id:
                        raise self.exceptions('Found invalid key at position %s. '
                                              'Resulting key: "%s".' % (i, key))

            tally, results = 0, []
            for key in target_keys:

                # pull event from storage
                raw_ev = raw.Event.get(key)

                # null events are returned as empty structures
                if not raw_ev:
                    results.append(raw.Event())
                    continue

                tally += 1  # otherwise, it's a result (only increment count in this case)
                results.append(raw_ev)

            # return with materialized count and event list
            return messages.RawEvents(count=tally, events=results)

        except self.exceptions.generic as e:

            self.logging.error('Encountered bound service exception %s: %s.' % (e.__class__.__name__, str(e)))
            raise  # locally-bound exceptions can be re-raised safely

        except Exception as e:

            context = (e.__class__.__name__, str(e))
            self.logging.error('Encountered unhandled, unbound exception: (%s, %s).' % context)
            raise self.exceptions.generic('Encountered unhandled exception "%s": %s.' % context)

    @rpc.method(rpc.messages.VoidMessage, messages.RawEvents)
    def get_all(self, request):

        ''' Retrieve all known :py:class:`raw.Event` entities. '''

        raise NotImplementedError('`EventTracker` Raw API does not yet support `get_all`.')
