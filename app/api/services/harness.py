# -*- coding: utf-8 -*-

'''
Harness API

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# 3rd party
import webapp2

# policy libraries
from policy import *

# protorpc
from protorpc import messages

# apptools
from apptools import rpc
from apptools import model
from apptools.util import datastructures

# tracker endpoints
from api.handlers.tracker import TrackerEndpoint
from api.handlers.tracker.legacy import LegacyEndpoint


#### +=+=+ Messages +=+=+ ####
class URLTestRequest(model.Model):

    ''' A request to test a bunch of URLs. '''

    spec = basestring, {'repeated': True}


class URLTestResult(model.Model):

    ''' A test result for a single URL. '''

    # basic identifying information
    key = basestring
    url = basestring, {'required': True}

    # error information
    code = basestring
    message = basestring

    # profile and request status
    status = basestring, {'required': True}
    profile = basestring


class URLTestResults(messages.Message):

    ''' A response to a request to test a bunch of URLs. '''

    results = messages.MessageField(URLTestResult.to_message_model(), 1, repeated=True)
    count = messages.IntegerField(2, default=0)
    successes = messages.IntegerField(3, default=0)
    failures = messages.IntegerField(4, default=0)


#### +=+=+ Exceptions +=+=+ ####
class HarnessException(rpc.remote.ApplicationError):

    ''' Abstract root for all ``HarnessService``-based exceptions. '''

    pass


class NoTestURLs(HarnessException):

    ''' Raised when there are no URLs to test. '''

    pass


class InvalidURL(HarnessException):

    ''' Raised when an invalid URL is encountered for testing. '''

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
        'no_urls': NoTestURLs,
        'invalid_url': InvalidURL
    })

    @rpc.method(URLTestRequest, URLTestResults)
    def test_urls(self, request):

        ''' Pass a set of URLs through a test routine.

            :param request: :py:class:`URLTestRequest` message for
            the current request.

            :returns: :py:class:`URLTestResults` message for the
            current request. '''

        if not len(request.spec):
            raise self.exceptions.no_urls('No test URLs provided.')

        test_results = []
        for spec in request.spec:

            try:

                # filter out `http://`
                usplit = spec.split('//')
                rightwindow = usplit[1] if (len(usplit) == 2) else usplit[0]

                # split by url components, drop domain
                usplit = rightwindow.split('/')
                rightwindow = '/'.join(usplit[1:]) if (len(usplit) > 1) else None

                # fail if it's _just_ a domain
                if not rightwindow:
                    raise self.exceptions.invalid_url('Invalid URL encountered: "%s". Could not detect PATH.' % spec)

                # split out params to work with prefix
                endpoint, querystring = tuple(rightwindow.split('?'))

                if endpoint in ('image.php', 'serverpixel.php'):
                    legacy = True  # it's a legacy pixel
                    endpoint = '__legacy'

                else:
                    legacy = False  # it's a modern pixel
                    endpoint = '__tracker'

                # fail with no ref
                upath = '/'.join(['', '?'.join([endpoint, querystring])])
                if 'ref' not in upath and 'ix' not in upath:
                    error = 'Invalid URL encountered: "%s". Could not find REF code or sentinel.'
                    raise self.exceptions.invalid_url(error % upath)

                # factory request, delegate execution
                urequest, uresponse = webapp2.Request.blank(upath), webapp2.Response()

                # init handler
                handler = LegacyEndpoint(urequest, uresponse) if legacy else TrackerEndpoint(urequest, uresponse)
                handler.initialize(urequest, uresponse)

                try:
                    profile, result, event = handler.get(explicit=True)

                except Exception as e:
                    test_results.append(URLTestResult.to_message_model()(**{
                        'url': spec,
                        'code': e.__class__.__name__,
                        'message': str(e),
                        'status': 'error'
                    }))

                else:
                    urlsafe = event.key.urlsafe()
                    test_results.append(URLTestResult.to_message_model()(**{
                        'url': spec,
                        'status': 'success',
                        'profile': profile.__definition__,
                        'key': ' '.join([''.join(list(urlsafe)[(len(urlsafe) - 16):]), '...']),
                    }))

            except HarnessException as e:
                test_results.append(URLTestResult.to_message_model()(**{
                    'url': spec,
                    'code': e.__class__.__name__,
                    'message': str(e),
                    'status': 'error'
                }))

        return URLTestResults(**{
            'count': len(test_results),
            'results': test_results,
            'failures': len(filter(lambda x: x.status == 'error', test_results)),
            'successes': len(filter(lambda x: x.status != 'error', test_results))
        })
