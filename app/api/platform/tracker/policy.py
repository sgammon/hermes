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

            :param *args: Argument rollup to be passed in as
            positional formatting arguments.

            :param **kwargs: Keyword arguments. Can contain ``event``
            and ``exception`` properties to attach to ``warn`` call.

            :raises: Exception passed-in via ``exception`` key of
            ``kwargs``, if ``strict`` mode is active.

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

        ''' Extracts an HTTP Etag from ``request``,
            an :py:class:`webob.Request`, at chunkname
            ``identifier``.

            :param request: Source :py:class:`webob.Request`
            to pull *Etag* from.

            :param identifier: Chunkname to pull from *Etag*
            at ``request``, if any.

            :raises NotImplementedError: Always, as this
            method is currently stubbed.

            :returns: Decoded value for chunk identified
            by ``identifier`` embedded in the *Etag*
            attached to ``request``. '''

        # @TODO(sgammon): etag extractor
        if self.config.get('strict', True):
            self.logging.info('Extracting ETAG at identifier "%s".' % identifier)
        raise NotImplementedError('`EventTracker` does not yet support etag-based extraction.')

    def _extract_http_path(self, request, identifier):

        ''' Extracts a value from an HTTP path component,
            (hopefully) to be found in ``request``, a
            :py:class:`webob.Request`. Extracts value
            from path component at ``identifier``.

            :param request: Descendent of :py:class:`webob.Request`
            to pull HTTP path value from.

            :param identifier: Name of path component to retrieve
            value from.

            :raises NotImplementedError: Always, as this method
            is currently stubbed.

            :returns: Decoded value for HTTP path component
            retrieved from ``request`` at ``identifier`` '''

        # @TODO(sgammon): path extractor
        if self.config.get('strict', True):
            self.logging.info('Extracting PATH component at identifier "%s".' % identifier)
        raise NotImplementedError('`EventTracker` does not yet support path-based extraction.')

    def _extract_http_header(self, request, identifier):

        ''' Extracts a value from an HTTP header,
            (hopefully) to be found in ``request``
            (a :py:class:`webob.Request` descendent)
            at the header name ``identifier``.

            :param request: Class descendent of
            :py:class:`webob.Request` to pull header value
            from.

            :param identifier: Name of HTTP header to pull
            value at.

            :returns: Value at ``identifier``, or ``None``
            if the value could not be found. '''

        # @TODO(sgammon): header extractor
        self.logging.debug('Extracting HEADER at identifier "%s".' % identifier)
        return request.headers.get(identifier)

    def _extract_http_cookie(self, request, identifier):

        ''' Extracts a value from an HTTP cookie,
            (hopefully) to be found in ``request``
            (a :py:class:`webob.Request` descendent)
            at the cookie name ``identifier``.

            :param request: Class descendent of
            :py:class:`webob.Request` to pull cookie
            value from.

            :param identifier: Name of the HTTP cookie
            to pull value at.

            :returns: Value at cookie ``name``, from
            ``request``, or ``None`` if no such value
            could be found. '''

        # @TODO(sgammon): cookie extractor
        self.logging.debug('Extracting COOKIE at identifier "%s".' % identifier)
        return request.cookies.get(identifier)

    _http_extractors = {
        http.DataSlot.ETAG: _extract_http_etag,
        http.DataSlot.HEADER: _extract_http_header,
        http.DataSlot.COOKIE: _extract_http_cookie,
        http.DataSlot.PATH: _extract_http_path
    }


    ### ==== Public Methods ==== ###
    def match_parameters(self, data, policy, legacy=False):

        ''' Match parameter ``data`` from an active
            request to ``EventTracker`` to one or
            multiple :py:class:`Profile` descendents,
            starting with ``policy``.

            :param data:
            :param policy:
            :param legacy:

            :raises InvalidParamName: In the case of
            an invalid or empty parameter name.

            :raises DuplicateParameterName: In the case
            of a property name that occurred more than
            once, which is not allowed.

            :raises StopIteration: When available parameter
            specs have been completely exhausted.

            :returns: Recursively yields matched parameter
            classes. '''

        # initialize vars
        paramset, artifacts, converters, _mappers = [], {}, {}, set()

        # gather parameter artifacts and long-form identifiers
        for prm in policy.parameters:
            prefix = prm.config.get('category', '')  # grab category prefix
            name = prm.config.get('name', False)

            if name is False:  # default to using parameter full name
                name = prm.name

            if name in (None, False, '', [], set(), tuple(), frozenset()) or not isinstance(name, (
                    basestring, list, set, tuple, frozenset)):

                raise exceptions.InvalidParamName("Invalid property name for parameter '%s'."
                                                  " Found name of type '%s'." % (parameter, type(name)))

            if isinstance(name, (set, tuple, list, frozenset)):
                if isinstance(name, (set, frozenset)):
                    name = tuple(name)
                name = name[0]  # start with first available name

            # resolve value converter
            if prm.basetype is not None:
                if prm.basetype == basestring:
                    converter = unicode
                else:
                    converter = prm.basetype
            else:
                converter = lambda x: x

            if prm.mapper:
                converter = (prm.mapper, converter)

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
                if artifacts[name] is not prm:
                    raise exceptions.DuplicateParameterName("Encountered more than one parameter with the name "
                                                            "'%s' (violating property was '%s'." % (identifier, name))

            artifacts[identifier], converters[identifier] = prm, converter  # add to artifacts, converters

        # special HTTP stuff should be extracted by now, so it's okay to overwrite
        # the request with params, a ``dict``-like object.
        if isinstance(data, webob.Request):
            data = data.params

        expected = set(artifacts.keys())  # properties are gathered, build lookup list
        parameters = set(data.keys())  # grab and freeze data parameters

        valid = expected & parameters  # match all valid parameters via set intersection
        no_value = expected - valid  # match spec'd parameters with no present value
        no_schema = parameters - expected  # match parameters with no presence in the spec

        _done = set()
        for i in valid:  # process valid parameters
            _done.add(i)
            yield artifacts[i], converters[i], data[i]  # grab parameter, converter and value

        # check for iterable names
        for _id, prm_permutation in artifacts.iteritems():
            if isinstance(prm_permutation.config.get('name', name), (set, tuple, list, frozenset)):
                for next in prm_permutation.config.get('name', name):
                    if next in _done:
                        continue
                    if next in parameters:
                        _done.add(_id)
                        valid.add(_id)
                        if _id in no_value: no_value.remove(_id)
                        if _id in no_schema: no_value.remove(_id)
                        yield artifacts[_id], converters[_id], data[next]

        if no_value or no_schema:  # process invalid parameters, if any

            for i in no_value:

                param = artifacts[i]  # grab parameter

                if param.basevalue is not None:
                    yield param, param.basetype, param.basevalue
                else:

                    if isinstance(param.config.get('name'), (list, set, frozenset, tuple)):
                        prm_n = param.config.get('name')
                        context = [
                            "Expected property \"%s\" with primary name \"%s\" (and name options %s) was not found.",
                            param.name,
                            i,
                            ', '.join(map(lambda s: '"%s"' % s, prm_n))
                        ]

                    else:
                        context = ["Expected property \"%s\" (at name \"%s\") was not found.", param.name, i]

                    # check if this is an enforced/required property
                    if param.config.get('policy', parameter.ParameterPolicy.OPTIONAL) in (
                            parameter.ParameterPolicy.REQUIRED, parameter.ParameterPolicy.ENFORCED):
                        yield param, exceptions.MissingParameter, context

                    else:
                        # if it's not a strict field, don't except
                        yield param, None, context

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
        raw, pipe = self.bus.event.raw(data, policy=base_policy, legacy=legacy)
        tracker = self.bus.resolve(raw, base_policy, legacy)

        # persist raw entity
        rkey, pipe = self.bus.engine.persist(raw, pipeline=pipe)

        # by this point, raw event has already been ``put`` and ``published``. start building tracked event.
        ev = event.TrackedEvent(**{
            'key': model.Key(event.TrackedEvent, raw.key.id),
            'raw': raw.key.urlsafe(),
            'params': {},
            'warnings': [],
            'errors': [],
            'profile': base_policy.__definition__,
            'modified': datetime.datetime.now(),
            'created': datetime.datetime.now()
        })

        # first, process parameters
        data_parameters = {}

        try:
            _deferred_mappers = []
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
                            if isinstance(followup, tuple):  # it's a mapper, defer it until later
                                followup, converter = followup
                                _deferred_mappers.append((param.name, followup, converter, data))

                            else:  # it's a basetype
                                if followup is basestring:
                                    followup = unicode

                                # convert types/call mappers and assign to data properties
                                data_parameters[param.name] = followup(data)

                    except ValueError as e:
                        message = 'Error converting param "%s" (with value "%s") using `%s`. Exception: "%s".'
                        self._strictwarn(message, param.name, data, followup, str(e), event=ev)
                        continue

            # run deferred mappers
            for prm_name, followup, converter, data in _deferred_mappers:

                try:
                    if converter is basestring:
                        converter = unicode
                    data_parameters[prm_name] = followup(ev, data_parameters, converter(data))

                except ValueError as e:
                    message = 'Error converting param "%s" (with mapper, and value "%s"). Exception: "%s".'
                    self._strictwarn(message, param.name, str(e))
                    continue

        except exceptions.PolicyEngineException as e:

            self.logging.info('Dropping pipelined commands for error codepath.')
            pipe = None  # clear pipelined commands, something went terribly wrong

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
                    self.bus.stream.publish(raw, error=True, execute=True, pipeline=False, propagate=True)
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

                raise  # re-raise

            # if we're in strict mode, re-raise errors
            if self.config.get('strict', True):
                raise  # re-raise

        else:

            # everything worked I guess! copy over parameters.
            ev.params = data_parameters

            # calculate aggregation specs
            ev.aggregations = []
            for aggr_policy in base_policy.aggregations:
                for delta, spec in aggr_policy.build(base_policy, ev):
                    for subspec in spec:

                        # write each aggregation increment
                        pipe = self.bus.engine.increment(subspec, delta, pipe)
                        ev.aggregations.append(subspec)

            # calculate attribution specs
            #for spec in base_policy.attributions:
            #    print "Would attribute: %s" % spec

            # return tupled <raw>, <tracker>, <ev>
            return raw, tracker, ev, pipe
