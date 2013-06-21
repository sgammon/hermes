# -*- coding: utf-8 -*-

# protorpc / mappers
from apptools.rpc import mappers
from protorpc import transport

# services
from . import raw
from . import event
from . import tracker


## APIClient
# Wrapper and master API client singleton object.
class APIClient(object):

    ''' Singleton class for use as a universal API
        client library wrapper. '''

    services = (
        ('raw', raw.RawDataService),
        ('event', event.EventDataService),
        ('tracker', tracker.TrackerService)
    )

    def __init__(self, host='amp.sh', endpoint='/v1/rpc', https=True, port=None):

        ''' Initialize this :py:class:`APIClient`.

            :param host: Host to send API requests to. Defaults to ``amp.sh``.
            :param endpoint: URL endpoint prefix for services. Defaults to ``/v1/rpc``.
            :param https: Flag indicating ``HTTPS`` mode.
            :param port: Port number override - must be ``int``.
            :returns: Nothing, as this is a constructor. '''

        # build config
        if port is None: port = 443 if https else 80
        endpoint_prefix = ''.join([('https://' if https else 'http://'), ':'.join([host, str(port)]), endpoint])

        # set up service stubs
        for name, api in self.services:
            api_endpoint = '/'.join([endpoint_prefix, name])
            setattr(self, name, api.Stub(transport.HttpTransport(api_endpoint, protocol=mappers.JSONRPC)))

    @classmethod
    def local(cls, **kwargs):

        ''' Generate a local :py:class:`APIClient` for use
            during development and testing. Default settings
            for local use are:

            * Host == ``127.0.0.1``
            * Endpoint == ``/v1/rpc``
            * HTTPS == ``False``
            * Port == ``8080``

            :param **kwargs: Keyword arguments to layer on
            to the constructor.

            :returns: Constructed :py:class:`APIClient`. '''

        return cls(*(
            kwargs.get('host', '127.0.0.1'),
            kwargs.get('endpoint', '/v1/rpc'),
            kwargs.get('https', False),
            kwargs.get('port', 8080)
        ))
