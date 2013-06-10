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

# stdlib
import webob
import datetime

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

    _config_path = 'tracker.policy.PolicyEngine'  # @TODO(sgammon): document config structure (``strict``/``debug``)

    ### ==== Internal Methods ==== ###

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

    ### ==== HTTP-related Internals ==== ###

    def _extract_http_etag(self, request, identifier):

        ''' Extracts an HTTP Etag. '''

        # @TODO(sgammon): etag extractor
        self.logging.info('Extracting ETAG at identifier "%s".' % identifier)
        raise NotImplementedError('`EventTracker` does not yet support etag-based extraction.')

    def _extract_http_path(self, request, identifier):

        ''' Extracts an HTTP path component. '''

        # @TODO(sgammon): path extractor
        self.logging.info('Extracting PATH component at identifier "%s".' % identifier)
        raise NotImplementedError('`EventTracker` does not yet support path-based extraction.')

    def _extract_http_header(self, request, identifier):

        ''' Extracts an HTTP header. '''

        # @TODO(sgammon): header extractor
        self.logging.info('Extracting HEADER at identifier "%s".' % identifier)
        return request.headers.get(identifier)

    def _extract_http_cookie(self, request, identifier):

        ''' Extracts an HTTP cookie. '''

        # @TODO(sgammon): cookie extractor
        self.logging.info('Extracting COOKIE at identifier "%s".' % identifier)
        return request.cookies.get(identifier)

    _http_extractors = {
        http.DataSlot.ETAG: _extract_http_etag,
        http.DataSlot.HEADER: _extract_http_header,
        http.DataSlot.COOKIE: _extract_http_cookie,
        http.DataSlot.PATH: _extract_http_path
    }


    ### ==== Public Methods ==== ###

    def match_parameters(self, data, policy, legacy=False):

        ''' Blab '''

        # initialize vars
        paramset, artifacts, converters = [], {}, {}

        # gather parameter artifacts and long-form identifiers
        for prm in policy.parameters:
            prefix = prm.config.get('category', '')  # grab category prefix
            name = prm.config.get('name', False)

            if name is False:  # default to using parameter full name
                name = prm.name

            if name in (None, False, '') or not isinstance(name, basestring):
                raise exceptions.InvalidParamName("Invalid property name for parameter '%s'."
                                                  " Found name of type '%s'." % (parameter, type(name)))

            # resolve value converter
            if prm.basetype is not None:
                if prm.basetype == basestring:
                    converter = unicode
                else:
                    converter = prm.basetype
            else:
                converter = lambda x: x

            # http.DataSlot.PARAM == 1 (all special slots are >1)
            # http.DataSlot.PATH == 0x5 (maximum, anything above this bound is invalid)
            if isinstance(data, webob.Request) and prm.config.get('source', 0) > 1 < 0x5:

                # it's an HTTP request with a special extractor. extract the value, yield with param and converter.
                yield prm, converter, self._http_extractors[prm.config['source']](self, data, name)
                continue  # advance parameter processing loop

            # compute identifier
            identifier = prm.config.get('separator', '').join([prefix, name]) if prefix else name

            # add to artifacts to look for
            if name in artifacts:
                raise exceptions.DuplicateParameterName("Encountered more than one parameter with the name "
                                                        "'%s' (violating property was '%s'." % (identifier, name))

            artifacts[identifier], converters[identifier] = prm, converter  # add to artifacts, converters

        # special HTTP stuff should be extracted by now, so it's okay to overwrite
        # the request with params, a ``dict``-like object.
        if isinstance(data, webob.Request):
            data = data.params

        expected = frozenset(artifacts.keys())  # properties are gathered, build lookup list
        parameters = frozenset(data.keys())  # grab and freeze data parameters

        valid = expected & parameters  # match all valid parameters via set intersection
        no_value = expected - (parameters - valid)  # match spec'd parameters with no present value
        no_schema = parameters - expected  # match parameters with no presence in the spec

        for i in valid:  # process valid parameters
            yield artifacts[i], converters[i], data[i]  # grab parameter, converter and value

        if no_value or no_schema:  # process invalid parameters, if any

            for i in no_value:
                param = artifacts[i]  # grab parameter
                message = 'Expected property "%s" (at name "%s") was not found.'

                # check if this is an enforced/required property
                if prm.config.get('policy', parameter.ParameterPolicy.OPTIONAL) in (
                        parameter.ParameterPolicy.REQUIRED, parameter.ParameterPolicy.ENFORCED):
                    yield param, exceptions.MissingParameter, (message, param.name, i)

                else:
                    # if it's not a strict field, don't except
                    yield param, None, (message, param.name, i)

            for i in no_schema:
                if i == 'ref' and legacy:
                    continue  # special case: ``ref`` property
                message = 'Received unexpected parameter "%s" with value "%s".'
                yield param, exceptions.UnexpectedParameter, (message, i, data.get(i))

        raise StopIteration()  # we're done here

    def enforce(self, data, base_policy, legacy=False):

        ''' Gather, build, enforce and map policy for the
            given :py:class:`model.tracker.Tracker` and
            :py:class:`model.raw.Event`.

            :param data: Can either be a ``dict`` of key=>value
            pairs, or a :py:class:`webapp2.Request`, in the case
            we're operating in an HTTP context.

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
            :py:class:`model.event.TrackedEvent`, assuming related policy
            applies properly, and the ``raw`` event and ``tracker``
            associated with it, in the form of: ``tuple(<raw>, <tracker>, <event>)``. '''

        # resolve tracker, build raw event
        raw = self.bus.event.raw(data, policy=base_policy, legacy=legacy)
        tracker = self.bus.resolve(raw, base_policy, legacy)

        # by this point, raw event has already been ``put`` and ``published``. start building tracked event.
        ev = event.TrackedEvent(**{
            'key': model.Key(event.TrackedEvent, raw.key.id),
            'raw': raw.key.urlsafe(),
            'params': {},
            'warnings': [],
            'errors': [],
            'modified': datetime.datetime.now(),
            'created': datetime.datetime.now()
        })

        # first, process parameters
        data_parameters = {}

        try:
            for param, followup, data in self.match_parameters(data, base_policy, legacy):

                # check if we're dealing with a warning
                if followup is None:
                    self._strictwarn(data[0], *data[1:], exception=None, event=ev)
                    continue

                # check if we're dealing with an exception
                if isinstance(followup, type) and issubclass(followup, exceptions.PolicyEngineException):

                    # delegate to warning/exception
                    self._strictwarn(data[0], *data[1:], exception=followup, event=ev)

                else:
                    try:

                        if data is None:
                            data_parameters[param.name] = data
                        else:
                            # convert types and assign to data properties
                            data_parameters[param.name] = followup(data)

                    except ValueError as e:
                        message = 'Error converting param "%s" (with value "%s") using `%s`. Exception: "%s".'
                        self._strictwarn(message, param.name, data, followup, str(e), event=ev)

        except exceptions.PolicyEngineException as e:

            # things that get out to this level should always be re-raised
            message = 'Encountered unhandled exception "%s": %s' % (e.__class__.__name__, str(e))
            self.logging.error(message)

            # mark raw and event as errors
            ev.errors.append(message)
            ev.error = True
            raw.error = True

            # save raw, attempt to save tracked
            keys = (raw.key.urlsafe(), ev.key.urlsafe())
            self.logging.error('Marking RAW and FULL events as errors, committing at keys "%s" and "%s".' % keys)

            try:
                raw.put()
            except:
                self.logging.critical('Critical persistence failure for raw event at key: "%s"' % raw.key)
                self.logging.critical('Event<%s>' % str(raw))
                self.logging.critical('Data<%s>' % str(data))
            else:
                self.logging.info('RAW event saved successfully.')
                self.logging.info('Publishing RAW event as error.')

                # publish RAW event
                try:
                    self.bus.stream.publish(raw, error=True, propagate=True)
                except:
                    self.logging.critical('Failed to publush RAW error event.')
                else:
                    self.logging.info('RAW error event published.')

                    # if RAW event was saved and published, attempt to save FULL event
                    try:
                        ev.put()
                    except:
                        self.logging.error('Failed to persist FULL event at key: "%s".' % ev.key)
                        self.logging.error('TrackedEvent<%s>' % ev)
                    else:
                        self.logging.info('FULL event saved successfully.')

            # if we're in strict mode, re-raise errors
            if self.config.get('strict', True):
                raise

        else:

            # everything worked I guess! copy over parameters.
            ev.params = data_parameters

            # calculate aggregation specs
            aggregations = []
            for aggr_policy in base_policy.aggregations:
                for delta, spec in aggr_policy.build(base_policy, ev):
                    for subspec in spec:
                        aggregations.append((spec, delta))
                        print "Would increment '%s' by '%s'." % (subspec, delta)

            # calculate aggregation specs
            #for spec in base_policy.attributions:
            #    print "Would aggregate: %s" % spec

        # return tupled <raw>, <tracker>, <ev>
        return raw, tracker, ev
