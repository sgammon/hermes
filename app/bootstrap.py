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

            :returns: :class:`AppBootstrapper`. '''

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
        from apptools.api import output
        from apptools.api import assets
        from apptools.api import services

        # === AppTools Extensions === #
        from apptools import ext

        # === AppTools Utilities === #
        from apptools import util
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

        # === AppTools Platform === #
        from apptools import platform
        from apptools.platform import generic
        from apptools.platform import appengine
        from apptools.platform import appfactory

        # === AppTools RPC === #
        from apptools import rpc
        from apptools.rpc import mappers
        from apptools.rpc import dispatch

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
            from api.models import harness
        except:
            if _DEBUG:
                raise
            else:
                pass

        try:
            # === API Platforms === #
            from api import platform
            from api.platform import hermes
            from api.platform import tracker
        except:
            if _DEBUG:
                raise
            else:
                pass

        # === API Services === #
        from api import services
        __import__('api.services', globals(), locals(), ['*'], 0)

        try:
            # Raw Data Service
            from api.services import raw
            from api.services.raw import service, messages, exceptions
        except:
            if _DEBUG:
                raise
            else:
                pass

        try:
            # Event Data Service
            from api.services import event
            from api.services.event import service, messages, exceptions
        except:
            if _DEBUG:
                raise
            else:
                pass

        try:
            # Eventstream Pub/Sub Service
            from api.services import pubsub
            from api.services.pubsub import service, messages, exceptions
        except:
            if _DEBUG:
                raise
            else:
                pass

        try:
            # Tracker Service
            from api.services import tracker
            from api.services.tracker import service, messages, exceptions
        except:
            if _DEBUG:
                raise
            else:
                pass

        try:
            # Harness Service
            from api.services import harness
        except:
            if _DEBUG:
                raise
            else:
                pass

        try:
            # === API Templates === #
            from api.templates import compiled
        except:
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
                pass

        return cls

AppBootstrapper.prepareImports()
