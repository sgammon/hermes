# -*- coding: utf-8 -*-

"""
This package contains platform classes. AppTools platform classes contain
business logic code that must be distributed to all base classes in an app.
Platforms are registered at ``apptools.system.platform``, and are picked up
and injected at class construction time, such that platform functionality
is ready and waiting when ``self`` is defined at runtime.

Interface
---------

Platforms can export a number of special methods and properties. These
attributes are picked up and considered by the ``apptools`` platform
runtime (see: :py:mod:`apptools.util.platform`):

  * :py:meth:`Platform.check_environment`:

    Executed by apptools internals before injection and after import,
    to delegate environment compatibility detection to the Platform.
    Must return ``True`` or ``False`` to indicate whether this platform
    can (and should) be loaded::

        # -*- coding: utf-8 -*-

        ## SamplePlatform - sample platform for the docs.
        class SamplePlatform(object):

            ''' Our cool sample platform. '''

            @classmethod
            def check_environment(cls, environ, config):

                ''' Check for some import that this platform depends on. '''

                try:
                    import cool_package
                except ImportError as e:
                  return False
                return True


  * :py:attr:`Platform.shortcut_exports`:

    Accessed by apptools internals. Must be a structure in the format
    ``[(<string>, <obj>)]``. Shortcuts exported in this way
    will appear on injected base classes as directly attached at the
    top-level of the object's dict. For example::

        # -*- coding: utf-8 -*-

        ## SamplePlatform - export some shortcuts.
        class SamplePlatform(object):

            ''' Sample platform that exports shortcuts. '''

            @property
            def shortcut_exports(self):

                ''' Return exported base class shortcuts. '''

                return [('api', self.api), ('my_cool_platform', self)]


    And then, many microseconds later, in a handler far, far away... a wild
    platform magically appears::

        # -*- coding: utf-8 -*-

        ## MyHandler - cool handler demo-ing Platforms.
        class MyHandler(WebHandler):

            ''' My cool injected handler. '''

            def get(self):

                ''' HTTP GET '''

                self.api == MyPlatform.api  # this is truthy
                self.my_cool_platform == MyPlatform  # this is also truthy


  * :py:attr:`Platform.template_context`:

    Loaded by the AppTools output API to allow a Platform to inject data
    into the global Jinja2 template context. This is evaluated at runtime
    during the request processing flow, and thus has access to request
    environment data. Must return a closure to be executed during render,
    that accepts the parameters ``handler`` (the current handler) and
    ``context`` (the current Jinja2 context), the latter of which **MUST** be
    mutated in place and passed back::

        # -*- coding: utf-8 -*-

        ## SamplePlatform - export some template context.
        class SamplePlatform(object):

            ''' Sample platform that exports template context entries. '''

            @property
            def template_context(self):

                ''' Return some local data that we have. '''

                def inject_stuff(handler, context):

                    ''' Inject `mycoolvar` into the Jinja2 template context. '''

                    context['mycoolvar'] = 'wassup template!'

                return context


    And then, many microseconds later in a template far, far away... your
    stupid template variable is *waiting for you*:

    .. code-block :: jinja

          {% block injected %}
              <b>{{ mycoolvar }}</b>
          {% endblock injected %}

    Will produce the HTML:

    .. code-block :: html

        <ul>
            <li><b>mycooltemplate</b></li>
        </ul>


  * :py:attr:`Platform.config_shortcuts`:

    Loaded and attached by the apptools internals to base classes in a very
    similar way to ``shortcut_exports``. This structure, however, accepts
    a list of the form ``list(tuple(<string>, <obj>))``, where ``<string>``
    is a path to config. The resulting object is wrapped in a Webapp2 cached
    property and attached as a config shortcut.

    Mostly for internal use.


Hooks
---------

Platforms can also export method hooks, which are dispatched by ``apptools``
at various stages of the request/response execution flow:

    * :py:meth:`Platform.pre_dispatch`:
      Hook method that, if defined, is executed right before handler dispatch.
      The request flow can be stopped by raising an exception, but the return
      value of this function is ignored, so it's mostly for initialization.

      :param handler: The currently-active :py:class:`webapp.RequestHandler`.
      :returns: *Must* return the current handler.


    * :py:meth:`Platform.post_dispatch`:
      Hook method that, if defined, is executed right after the response is
      returned from the handler. Once again, the request flow can be stopped
      via exceptions but the return value is ignored.

      :param handler: The currently-active :py:class:`webapp.RequestHandler`.
      :param response: The currently-active :py:class:`webapp.Response`.
      :returns: Return value is discarded - since the request execution flow
                has already ceased, the return value from this method is
                discarded.



:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.

"""

# Base Imports
import config
import webapp2

# Utils
from apptools.util import debug
from apptools.util import decorators


## Platform - abstract platform class
class Platform(object):

    ''' Root abstract class for platform objects. '''

    def __init__(self):

        ''' Initialize this ``Platform`. '''

        if hasattr(self, 'initialize'):
            self.initialize()

    @decorators.classproperty
    def _config_path(cls):

        ''' Calculate dynamic default config path.

            :returns: String configuration path, which defaults to
                      concatenated module import path and class name
                      (for example: ``cool.platforms.Platform``). '''

        return '.'.join(cls.__module__.split('.') + [cls.__name__])

    @webapp2.cached_property
    def config(self):

        ''' Named config pipe. Resolves ``Platform`` configuration.

            :returns: Configuration ``dict`` for target ``Platform``.
                      In this case, ``debug`` always defaults to
                      ``True`` if no config was found. '''

        return config.config.get(self._config_path, {'debug': True})

    @webapp2.cached_property
    def logging(self):

        ''' Named logging pipe. Reads :py:attr:`PlatformBridge._config_path`
            to produce a customized log pipe.

            :returns: A brand new :py:class:`apptools.debug.AppToolsLogger`,
                      with the current ``path``/``name``/``condition`` set. '''

        _split = self._config_path.split('.')
        return debug.AppToolsLogger(**{
            'path': '.'.join(_split[0:-1]),
            'name': _split[-1]
        })._setcondition(self.config.get('debug', True))


## PlatformBridge - abstract class for objects held by platforms
class PlatformBridge(object):

    ''' Root abstract class for platform objects. '''

    bus = None
    handler = None

    def __init__(self, bus=None):

        ''' Initialize a PlatformBridge, optionally with a parent bus.

            :param bus: Parent ``Platform``, for access to other bridges/main code. '''

        if bus:
            self.bus = bus

    @webapp2.cached_property
    def config(self):

        ''' Named config pipe. Reads :py:attr:`PlatformBridge._config_path`.

            :returns: Configuration ``dict`` for contextual class, if any.
                      Defaults to returning an empty dictionary. '''

        # Generate and return path by fully-qualified python module + class name (e.g. yoga.platform.PlatformBridge)
        return config.config.get(self._config_path, {})

    @webapp2.cached_property
    def logging(self):

        ''' Named logging pipe. Reads :py:attr:`PlatformBridge._config_path`
            to produce a customized log pipe.

            :returns: A brand new :py:class:`apptools.debug.AppToolsLogger`,
                      with the current ``path``/``name``/``condition`` set. '''

        return debug.AppToolsLogger(**{
            'path': self.__module__,
            'name': self.__class__.__name__
        })._setcondition(self.config.get('debug', True))

    @webapp2.cached_property
    def _config_path(self):

        ''' Generate a config path, like "python.module.to.Class" for a given class.

            :returns: String config path, built from module import path and class
                      name (for example: ``api.platform.ampush.example.Example``). '''

        return '.'.join([i for i in self.__module__.split('.')] + [self.__class__.__name__])
