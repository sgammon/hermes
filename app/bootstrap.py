# -*- coding: utf-8 -*-

"""
This small utility file is loaded by AppTools and executed as early
as possible in the execution flow, to facilitate the injection of
paths onto `sys.path`, preloading, and other process-level init for
the app.

It's dead simple to use::

    # -*- coding: utf-8 -*-

    import bootstrap
    bootstrap.AppBootstrapper.prepareImports().preload()


:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# stdlib
import sys

# Globals
_bootstrapped = False


## AppBootstrapper - does basic app startup/boot tasks.
class AppBootstrapper(object):

    ''' Performs early app bootstrap procedures, such as
        adding to :py:attr:`sys.path` and preloading
        :py:mod:`apptools`.

        Paths from :py:attr:`cls.injected_paths` are added to :py:attr:`sys.path`
        if they are not present. This class is designed to
        be idempotent - a module-global flag (*_bootstrapped*)
        is flipped once the bootstrapper has run.
    '''

    injected_paths = 'lib', 'lib/dist', '/momentum'

    @classmethod
    def prepareImports(cls):

        ''' Prepare Python import path.

            :returns: :class:`AppBootstrapper`.
        '''

        global _bootstrapped

        if not _bootstrapped:
            for p in cls.injected_paths:
                if p not in sys.path:
                    sys.path.append(p)
            _bootstrapped = True
        return cls

    @classmethod
    def preloadApptools(cls, _DEBUG=False):

        ''' Preload AppTools modules.

            :param _DEBUG:
                If truthy, re-raises *ImportErrors* encountered during
                the module preload routine. Defaults to ``False``.
            :returns: :py:class:`AppBootstrapper`.
            :raises: Re-raises :py:exc:`ImportError`.
        '''

        import apptools  # apptools, by momentum :)

        from apptools import core
        from apptools import dispatch
        from apptools import exceptions

        # === AppTools APIs === #
        from apptools import api

        # Output API (& extensions)
        from apptools.api import output
        from apptools.api.output import extensions
        from apptools.api.output.extensions import fragment
        from apptools.api.output.extensions import bytecache
        from apptools.api.output.extensions import memcached

        # Assets API
        from apptools.api import assets

        # Push API
        from apptools.api import push

        # Services API
        from apptools.api import services

        # === AppTools Extensions === #
        from apptools import ext

        # === AppTools Utilities === #
        from apptools import util
        from apptools.util import json
        from apptools.util import debug
        from apptools.util import runtools
        from apptools.util import appconfig
        from apptools.util import timesince
        from apptools.util import decorators
        from apptools.util import byteconvert
        from apptools.util import datastructures
        from apptools.util import httpagentparser

        # === AppTools Models === #
        from apptools import model
        from apptools.model import builtin
        from apptools.model import adapter
        from apptools.model.adapter import sql
        from apptools.model.adapter import core
        from apptools.model.adapter import redis
        from apptools.model.adapter import mongo
        from apptools.model.adapter import abstract
        from apptools.model.adapter import protorpc
        from apptools.model.adapter import pipeline
        from apptools.model.adapter import inmemory
        from apptools.model.adapter import memcache

        # === AppTools Platform === #
        from apptools import platform
        from apptools.platform import generic
        from apptools.platform import appengine
        from apptools.platform import appfactory

        # === AppTools Services === #
        from apptools import services
        from apptools.services import builtin
        from apptools.services import gateway
        from apptools.services import mappers
        from apptools.services import realtime
        from apptools.services import middleware

        return cls

    @classmethod
    def preloadHermes(cls, _DEBUG=False):

        ''' Preload Hermes modules.

            :keyword _DEBUG:
                If truthy, re-raises *ImportErrors* encountered during
                the module preload routine. Defaults to ``False``.
            :returns: :py:class:`AppBootstrapper`.
            :raises: :py:exc:`ImportError` if ``_DEBUG`` is ``True``
                     and a descendent of :py:exc:`ImportError` is
                     encountered during execution.
        '''

        import api  # Project: Hermes

        # === API Top-Level === #
        from api import routing
        from api import exceptions

        # === API Handlers === #
        from api import handlers
        from api.handlers import harness

        # === API Messages === #
        from api import messages

        # === API Middleware === #
        from api import middleware

        # ==== API Models ==== #
        from api import models
        from api.models import harness

        try:
            # Tracker Models
            from api.models import tracker
            from api.models.tracker import raw
            from api.models.tracker import event
            from api.models.tracker import pubsub
            from api.models.tracker import profile
            from api.models.tracker import tracker
            from api.models.tracker import parameter
            from api.models.tracker import integration
            from api.models.tracker import attribution
            from api.models.tracker import aggregation
        except:
            if _DEBUG:
                raise
            else:
                pass

        try:
            # === API Platforms === #
            from api import platform
            from api.platform import ampush
            from api.platform.ampush import hermes
            from api.platform.ampush import tracker
        except:
            if _DEBUG:
                raise
            else:
                pass

        # === API Services === #
        from api import services

        try:
            # Raw Data Service
            from api.services import raw
            from api.services.raw import service
            from api.services.raw import messages
            from api.services.raw import exceptions
        except:
            if _DEBUG:
                raise
            else:
                pass

        try:
            # Event Data Service
            from api.services import event
            from api.services.event import service
            from api.services.event import messages
            from api.services.event import exceptions
        except:
            if _DEBUG:
                raise
            else:
                pass

        try:
            # Eventstream Pub/Sub Service
            from api.services import pubsub
            from api.services.pubsub import service
            from api.services.pubsub import messages
            from api.services.pubsub import exceptions
        except:
            if _DEBUG:
                raise
            else:
                pass

        try:
            # Tracker Service
            from api.services import tracker
            from api.services.tracker import service
            from api.services.tracker import messages
            from api.services.tracker import exceptions
        except:
            if _DEBUG:
                raise
            else:
                pass

        try:
            # === API Templates === #
            from api.templates import compiled
            from api.templates.compiled import test
            from api.templates.compiled import core
            from api.templates.compiled import macros
            from api.templates.compiled import layout
            from api.templates.compiled import harness
        except:
            if _DEBUG:
                print "Failed to preload compiled templates."
            pass

        return cls

    @classmethod
    def preloadTracker(cls, _DEBUG=False):

        ''' Preload Tracker modules.

            :param _DEBUG:
                If truthy, re-raises *ImportErrors* encountered during
                the module preload routine. Defaults to ``False``.
            :returns: :py:class:`AppBootstrapper`.
            :raises: Re-raises :py:exc:`ImportError`.
        '''

        # === Tools === #
        import tools
        from tools import actor

        # === Components === #
        import components

        # Event / Tracker
        from components import event
        from components import tracker

        # Protocol
        from components import protocol
        from components.protocol import meta
        from components.protocol import http
        from components.protocol import event
        from components.protocol import param
        from components.protocol import tracker

        # Datastore
        from components import datastore
        from components.datastore import embedded

        return cls

    @classmethod
    def preload(cls, _DEBUG=False):

        ''' Preload important Python modules at construction time.

            :param _DEBUG:
                If truthy, re-raises *ImportErrors* encountered during
                the module preload routine. Defaults to ``False``.
            :returns: :py:class:`AppBootstrapper`.
            :raises: :py:exc:`ImportError` if ``_DEBUG`` is ``True`` and
                     a descendent of :py:exc:`ImportError` is encountered
                     while executing this sub-classmethods (such as
                     :py:meth:`cls.preloadApptools`).
        '''

        for name, routine in (('apptools', cls.preloadApptools), ('tracker', cls.preloadTracker), ('hermes', cls.preloadHermes)):
            try:
                routine(_DEBUG)  # preload modules
            except ImportError:
                print "ERROR: Failed to preload module bundle \"%s\"." % name
                if _DEBUG:
                    raise
                else:
                    pass
            else:
                if _DEBUG:
                    print "Preloaded module bundle: \"%s\"." % name

        return cls

AppBootstrapper.prepareImports()
