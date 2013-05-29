# -*- coding: utf-8 -*-

'''
The :py:class:`PolicyEngine` class handles the application and
enforcement of event policies. Execution flow for extracting
parameters, generating followup tasks, and aggregation /
attribution happens here.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''


# apptools model API
from apptools import model

# Protocol Suite
from protocol import http

# Platform Parent
from api.platform import PlatformBridge


## PolicyEngine - handles application and enforcement of schema policy.
class PolicyEngine(PlatformBridge):

    ''' Receives resultant/collapsed/materialized policy from
        :py:class:`platform.ampush.tracker.event.EventBuilder`,
        and manages execution flow for applying that policy. '''

    def build(self, policies):

        ''' Compile multiple :py:class:`model.profile.Profile`
            classes into a single, compound policy class.

            :param policies:
            :returns: '''

        pass

    def gather(self):

        ''' Walk the class inheritance chain and gather applicable
            :py:class:`model.profile.Profile` classes, for construction
            into a compound policy for handling an event.

            :param tracker:
            :param context:
            :returns: '''

        pass

    def enforce(self):

        ''' Given a materialized :py:class:`model.event.TrackedEvent`,
            enforce policy decisions, potentially raising exceptions
            encountered along the way.

            :param suite:
            :param strict:
            :returns: Boolean indicating whether the compound policy
                      was found to be valid. '''

        pass

    def interpret(self, request, tracker, base_policy=None):

        ''' Gather, build, enforce and map policy for the
            given :py:class:`model.tracker.Tracker` and
            :py:class:`model.raw.Event`.

            :param request:
            :param tracker:
            :returns: A newly-inflated and provably-valid
                      :py:class:`model.event.TrackedEvent` '''

        raw = self.bus.event.raw(request)

        # resolve tracker for this request
        tracker = self.bus.resolve(raw, request)

        paramset = []
        for parameter in base_policy.parameters:
            prefix = parameter.config.get('category', '')  # grab category prefix
            name = parameter.config.get('name', False)

            if not name:
                raise Exception("Invalid property name for parameter '%s'. Skipping." % parameter)

            # compute identifier
            identifier = ''.join([prefix, name])

            if parameter.config.get('source', http.DataSlot.PARAM) == http.DataSlot.PARAM:
                print "looking for param '%s' at compound name '%s'" % (parameter.name, identifier)
                paramset.append((parameter, request.params.get(identifier)))

            elif parameter.config.get('source') == http.DataSlot.HEADER:
                print "looking for header '%s' at name '%s'" % (parameter.name, name)
                paramset.append((parameter, request.headers.get(identifier)))

            elif parameter.config.get('source') == http.DataSlot.COOKIE:
                print "looking for cookie '%s' at name '%s'" % (parameter.name, name)
                paramset.append((parameter, request.cookies.get(name)))

        # factory a new model class to hold the data, assign to ``Redis``
        _klass_params = {k.name: k.basetype for k, value in paramset}
        _klass_params.update({'__adapter__': 'RedisAdapter'})

        evmodel = model.Model.__metaclass__.__new__(model.Model, "TrackedEvent", (model.Model,), _klass_params)

        # initialize new model
        ev = evmodel(**{k.name: value for k, value in paramset})

        # return tupled <raw>, <tracker>, <ev>
        return raw, tracker, ev

