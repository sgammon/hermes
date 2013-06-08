# -*- coding: utf-8 -*-

'''

Policy Base

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# policy core
from policy import core

# protocol bindings
from protocol import http
from protocol import event
from protocol import intake
from protocol import builtin
from protocol import timedelta
from protocol import environment

# protocol extensions
from protocol import response
from protocol import parameter
from protocol import decorators
from protocol import integration
from protocol import attribution
from protocol import aggregation


## Constants
_DEFAULT_COOKIE_NAME = "_amp"

# Default attribution / aggregation lookback window
_DEFAULT_LOOKBACK = (timedelta.TimeWindow.ONE_DAY,
                     timedelta.TimeWindow.ONE_WEEK,
                     timedelta.TimeWindow.TWO_WEEKS,
                     timedelta.TimeWindow.FOUR_WEEKS,
                     timedelta.TimeWindow.FOREVER)


## EventProfile
# Default Event Profile.
class EventProfile(core.AbstractProfile):

    ''' Root concrete :py:class:`EventProfile` class. This is
        the eventual inheritance target for all ``EventProfile``
        classes. '''

    class Base(parameter.ParameterGroup):

        ''' Parameter group for base tracker parameters. '''

        # Sentinel: flag indicating that the hit URL was generated by our systems.
        sentinel = basestring, {
            'policy': parameter.ParameterPolicy.ENFORCED,
            'source': http.DataSlot.PARAM,
            'name': builtin.TrackerProtocol.SENTINEL,
            'category': parameter.ParameterType.INTERNAL
        }

        # Type: represents the type of hit, such as "impression" or "click".
        type = basestring, {
            'policy': parameter.ParameterPolicy.REQUIRED,
            'source': http.DataSlot.PARAM,
            'name': builtin.TrackerProtocol.TYPE,
            'binding': event.EventType,
            'category': parameter.ParameterType.INTERNAL,
            'aggregations': [
                aggregation.Aggregation('events-by-type', interval=_DEFAULT_LOOKBACK)
            ]
        }

        # Mode: describes how to respond to base hits.
        mode = int, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'source': http.DataSlot.HEADER,
            'binding': response.ResponseMode,
            'name': builtin.TrackerHeaders.RESPONSE_MODE,
            'category': parameter.ParameterType.INTERNAL
        }

        # Provider: represents the ID string of the provider of this hit.
        provider = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'source': http.DataSlot.PARAM,
            'name': builtin.TrackerProtocol.PROVIDER,
            'binding': event.EventProvider,
            'category': parameter.ParameterType.INTERNAL,
            'aggregations': [
                aggregation.Aggregation('events-by-provider', interval=_DEFAULT_LOOKBACK)
            ]
        }

        # Tracker: represents the ID of the parent tracker for the current hit.
        tracker = basestring, {
            'policy': parameter.ParameterPolicy.REQUIRED,
            'source': http.DataSlot.PARAM,
            'name': builtin.TrackerProtocol.TRACKER,
            'category': parameter.ParameterType.AMPUSH,
            'aggregations': [
                aggregation.Aggregation('events-by-tracker',
                    interval=(timedelta.TimeWindow.TWO_WEEKS, timedelta.TimeWindow.FOUR_WEEKS),
                    permutations=[
                        ('by-type', 'Base.TYPE'),
                        ('by-provider', 'Base.PROVIDER')
                    ]
                )
            ]
        }

        # Contract: represents the contract scope which this hit should be recorded for.
        contract = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'source': http.DataSlot.PARAM,
            'name': builtin.TrackerProtocol.CONTRACT,
            'category': parameter.ParameterType.AMPUSH,
            'aggregations': [
                aggregation.Aggregation('events-by-contract', interval=_DEFAULT_LOOKBACK, permutations=[
                    ('by-type', 'Base.TYPE'),
                    ('by-tracker', 'Base.TRACKER'),
                    ('by-provider', 'Base.PROVIDER'),
                    ('by-type-by-provider', ('Base.TYPE', 'Base.PROVIDER'))
                ])
            ]
        }

    class Environment(parameter.ParameterGroup):

        ''' Parameter group for client browser environment. '''

        # OS: The operating system the browser is running in.
        os = basestring, {
            'policy': parameter.ParameterPolicy.PREFERRED,
            'source': http.DataSlot.PARAM,
            'name': environment.BrowserEnvironment.OS,
            'category': parameter.ParameterType.DATA,
            'aggregations': [
                aggregation.Aggregation('hits-by-os', interval=_DEFAULT_LOOKBACK)
            ]
        }

        # Arch: The underlying architecture of the host operating system (i.e. "x86-64").
        arch = basestring, {
            'policy': parameter.ParameterPolicy.OPTIONAL,
            'source': http.DataSlot.PARAM,
            'name': environment.BrowserEnvironment.ARCH,
            'category': parameter.ParameterType.DATA,
        }

        # Vendor: The author of the browser being used (i.e. "Google" for Chrome).
        vendor = basestring, {
            'policy': parameter.ParameterPolicy.PREFERRED,
            'source': http.DataSlot.PARAM,
            'name': environment.BrowserEnvironment.VENDOR,
            'category': parameter.ParameterType.DATA
        }

        # Browser: The software-name of the browser being used (i.e. "Safari" for Safari).
        browser = basestring, {
            'policy': parameter.ParameterPolicy.PREFERRED,
            'source': http.DataSlot.PARAM,
            'name': environment.BrowserEnvironment.BROWSER,
            'category': parameter.ParameterType.DATA,
            'aggregations': [
                aggregation.Aggregation('hits-by-browser', interval=_DEFAULT_LOOKBACK, permutations=[
                    ('by-os', 'Environment.OS'),
                    ('by-type', 'Base.TYPE'),
                    ('by-provider', 'Base.PROVIDER'),
                    ('by-provider-by-type', ('Base.PROVIDER', 'Base.TYPE'))
                ])
            ]
        }

    class System(parameter.ParameterGroup):

        ''' Parameter group for system state/configuration. '''

        channel = int, {
            'policy': parameter.ParameterPolicy.SPECIAL,
            'source': http.DataSlot.HEADER,
            'name': 'XAF-Channel',
            'category': parameter.ParameterType.INTERNAL,
            'binding': intake.InputChannel
        }

    class Funnel(parameter.ParameterGroup):

        ''' Models the ad/marketing funnel. '''

        # Adgroup: The Ampush adgroup ID that generated this ``Event``, if any.
        adgroup = basestring, {
            'policy': parameter.ParameterPolicy.REQUIRED,
            'source': http.DataSlot.PARAM,
            'name': builtin.TrackerProtocol.ADGROUP,
            'category': parameter.ParameterType.AMPUSH,
            'attributions': [
                attribution.Attribution(name='hits-by-browser', interval=_DEFAULT_LOOKBACK, permutations=[
                    ('by-consumer', 'Consumer.FINGERPRINT')
                ])
            ],
            'aggregations': [
                aggregation.Aggregation(name='hits-by-browser', interval=_DEFAULT_LOOKBACK, permutations=[
                    ('by-consumer', 'Consumer.FINGERPRINT')
                ])
            ]
        }

    class Consumer(parameter.ParameterGroup):

        ''' Models the end-consumer. '''

        # Fingerprint: The consumer profile fingerprint, either encountered or created.
        fingerprint = basestring, {
            'policy': parameter.ParameterPolicy.SPECIAL,
            'source': http.DataSlot.COOKIE,
            'name': _DEFAULT_COOKIE_NAME,
            'category': parameter.ParameterType.INTERNAL
        }
