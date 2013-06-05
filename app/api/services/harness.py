# -*- coding: utf-8 -*-

'''
Harness API

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# apptools
from apptools import rpc
from apptools import model
from apptools.util import datastructures

# policy libraries
from policy import core
from policy import base
from policy import click
from policy import conversion
from policy import impression


#### +=+=+ Request/Response Messages +=+=+ ####


## SpecRequest - expresses a request for a profile spec.
class SpecRequest(model.Model):

    ''' Request a specific profile specification. '''

    profile = basestring, {'required': True}


## SpecResponse - expresses a response to a request for a profile spec.
class SpecResponse(model.Model):

    ''' Response to a :py:class:`SpecRequest`. '''

    profile = basestring
    spec = dict
    html = basestring


## BuildRequest - expresses a request to build a URL.
class BuildRequest(model.Model):

    ''' Request to build a URL from a profile and filled-out spec. '''

    profile = basestring
    params = dict


## BuildResponse - expresses a built URL.
class BuildResponse(model.Model):

    ''' Response to a :py:class:`BuildRequest`. '''

    url = basestring


#### +=+=+ Exceptions +=+=+ ####
class HarnessException(rpc.remote.ApplicationError):

    ''' Abstract root for all ``HarnessService``-based exceptions. '''

    pass


class InvalidProfile(HarnessException):

    ''' Indicates that a provided profile path was invalid. '''

    pass


#### +=+=+ Service +=+=+ ####

## HarnessService - exposes routines for testing and probing `EventTracker` functionality.
@rpc.service
class HarnessService(rpc.Service):

    ''' Exposes methods for testing the `EventTracker` pipeline. '''

    name = 'harness'
    _config_path = 'hermes.api.harness.HarnessService'

    exceptions = datastructures.DictProxy(**{
        'generic': HarnessException,
        'invalid_profile': InvalidProfile
    })

    @rpc.method(SpecRequest, SpecResponse)
    def profile_spec(self, request):

        ''' Retrieve a profile spec, rendered in HTML. '''

        import pdb; pdb.set_trace()

        try:
            # attempt to import target profile
            profile = None
            for path, name in core.Profile.registry:
                if request.profile == '.'.join([path, name]):
                    profile = core.Profile.registry[(path, name)]
                    break

            # fail if we can' find it
            if not profile:
                raise self.exceptions.invalid_profile('Failed to resolve profile at path "%s".' % request.profile)

            # generate schema
            schema = profile.to_schema_struct()

            # generate HTML from profile, return that and struct
            return SpecResponse(**{
                'profile': request.profile,
                'spec': schema,
                'html': self.render('fragments/profile_spec.html', path=request.profile, spec=schema)
            })

        except HarnessException as e:
            raise  # re-raise harness exceptions

        except Exception as e:
            error = "Unhandled app-level exception of type '%s': %s"
            raise self.exceptions.generic(error % (e.__class__.__name__, str(e)))


    @rpc.method(BuildRequest, BuildResponse)
    def build_url(self, request):

        ''' Build a URL from a filled-out spec. '''

        pass
