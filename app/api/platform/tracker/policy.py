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
from protocol import parameter

# Event Models
from api.models.tracker import event

# Platform Parent + Exceptions
from api.platform import PlatformBridge
from api.platform.tracker import exceptions


## PolicyEngine - handles application and enforcement of schema policy.
class PolicyEngine(PlatformBridge):

    ''' Receives resultant/collapsed/materialized policy from
        :py:class:`platform.ampush.tracker.event.EventBuilder`,
        and manages execution flow for applying that policy. '''

    _config_path = 'tracker.policy.PolicyEngine'

    def _strictwarn(self, message, *args, **kwargs):

        ''' Be strict if we're running in ``strict`` mode,
            otherwise issue a ``debug`` message.

            .. note: If a ``strict`` key isn't found in config,
            ``strict`` mode defaults to being **activated**.

            :param message: String message to issue as the log message.

            :keyword exception: The exception class to throw in the case
            that we're running in ``strict`` mode.

            :returns: ``self``, for chainability. '''

        ev = kwargs.get('event', None)  # pull current event, if any
        exception = kwargs.get('exception', None)  # pull kwarg for exception

        if len(args):
            message = message % args

        if self.config.get('strict', True):  # default to ``strict`` being _on_
            self.logging.warning(message)
            ev.warnings.append(message)
            if exception is not None:  # if in ``strict`` and we have an exception, raise it with the message given
                raise exception(message)
        else:
            if exception is not None:  # if we're not in ``strict`` but there's an exception attached, log a warning
                self.logging.warning(message)
                ev.warnings.append(message)
            else:
                self.logging.debug(message)
                ev.warnings.append(message)
        return self

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

    def interpret(self, request, tracker, base_policy=None, legacy=False):

        ''' Gather, build, enforce and map policy for the
            given :py:class:`model.tracker.Tracker` and
            :py:class:`model.raw.Event`.

            :param request: Current :py:class:`webapp2.Request` object.

            :param tracker: Tracker object attached to this event.

            :param legacy: Mark this as a legacy hit.

            :raises InvalidParamName: In the case of a property name
            (that should be a string) with an invalid type, will *always*
            raise.

            :raises MissingParameter: In the case of a parameter that is
            expected to exist (*ParameterPolicy.REQUIRED* or even
            *ParameterPolicy.ENFORCED*), but was not found in the
            current request. **Only raised if operating in ``strict``
            mode, and *never* in production.** If we're in production
            or ``strict`` mode is off, we log a warning.

            :raises UnexpectedParameter: In the case of a parameter that
            is found on the ``request``, but was not expected or accounted
            for in applicable ``policy``, and thus has no associated
            behavior that can be dependably expected. **Only raised if
            operating in ``strict`` mode, and *never* in production.** If
            we're in production or ``strict`` mode is off, we log a warning.

            :returns: A newly-inflated and provably-valid
                      :py:class:`model.event.TrackedEvent`,
                      assuming related policy applies properly,
                      and the ``raw`` event and ``tracker``
                      associated with it, in the form of:
                      ``tuple(<raw>, <tracker>, <event>)``. '''

        import pdb; pdb.set_trace()

        raw = self.bus.event.raw(request, policy=base_policy, legacy=legacy)

        # resolve tracker for this request
        tracker = self.bus.resolve(raw, request)

        paramset = []
        for prm in base_policy.parameters:
            prefix = prm.config.get('category', '')  # grab category prefix
            name = prm.config.get('name', False)

            if name is False:  # default to using parameter full name
                name = prm.name

            if name in (None, False, '') or not isinstance(name, basestring):
                raise exceptions.InvalidParamName("Invalid property name for parameter '%s'."
                                                  " Found name of type '%s'." % (parameter, type(name)))

            # compute identifier
            identifier = ''.join([prefix, name])

            if prm.config.get('source', http.DataSlot.PARAM) == http.DataSlot.PARAM:
                paramset.append((prm, name, request.params.get(identifier)))

            elif prm.config.get('source') == http.DataSlot.HEADER:
                paramset.append((prm, name, request.headers.get(identifier)))

            elif prm.config.get('source') == http.DataSlot.COOKIE:
                paramset.append((prm, name, request.cookies.get(name)))

        # factory a new model class to hold the data, assign to ``Redis``
        _klass_params = {k.name: k.basetype for k, _name, value in paramset}
        _klass_params.update({'__adapter__': 'RedisAdapter', '__expando__': True})

        # factory and initialize dynamic trackedevent model
        evmodel = model.Model.__metaclass__.__new__(model.Model, "TrackedEvent", (event.TrackedEvent,), _klass_params)

        accounted_params = []
        ev = evmodel(key=model.Key('TrackedEvent', raw.key.id))
        ev.errors, ev.warnings = [], []

        for k, _name, value in paramset:

            # skip things with empty values and optional flags
            if value is None and prm.config.get('policy', parameter.ParameterPolicy.OPTIONAL) in (
                    parameter.ParameterPolicy.REQUIRED,
                    parameter.ParameterPolicy.ENFORCED):

                # @TODO: param policy enforcement here (OPTIONA/REQUIRED/ENFORCED/etc)
                # @TODO: should have options for explicitly setting a property to ``None``
                message = 'Expected property "%s" (at name "%s") was not found (got `None` as value) and will not be saved.'
                self._strictwarn(message, k.name, _name, exception=exceptions.MissingParameter, event=ev)
                continue

            converter = k.basetype
            if converter == basestring:  # special case: ``basestring`` cannot be constructed directly
                converter = unicode
            if converter is None:
                converter = lambda x: x  # special case: a ``None`` converter does no conversion

            try:
                ## assign value to property
                ev[k.name] = converter(value)
                accounted_params.append(_name)

            except ValueError as e:
                message = 'Encountered error converting param "%s" (with value "%s", type "%s", name "%s") with converter %s. Exception: "%s".'
                self._strictwarn(message, k.name, value, type(value), _name, converter, str(e), **{
                    'exception': exceptions.InvalidParameterValue,
                    'event': ev
                })

        for param in request.params:

            if legacy and param == 'ref':
                continue  # ref can be skipped in legacy situations (special case)

            if param not in accounted_params:

                # woops, there are extra params on the request for some reason (that are dropped)
                message = 'Found unexpected parameter "%s" (got "%s" as value).'
                self._strictwarn(message, param, request.params.get(param), **{
                    'exception': exceptions.UnexpectedParameter,
                    'event': ev
                })

        # return tupled <raw>, <tracker>, <ev>
        return raw, tracker, ev
