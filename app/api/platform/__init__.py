# -*- coding: utf-8 -*-

'''

API: Platforms

This package contains platform classes. AppTools platform classes contain
business logic code that must be distributed to all base classes in an app.
Platforms are registered at `apptools.system.platform`, and are picked up
and injected at class construction time, such that platform functionality
is ready and waiting when `self` is defined at runtime.

Platforms can export a number of methods and properties that let them hook
into core app functionality:

    -- [classmethod] `check_environment`(cls, <environ>, <config>)
        Executed by apptools internals before injection and after import,
        to delegate environment compatibility detection to the Platform.
        Must return True or False to indicate whether this platform should
        be loaded.

        Example:

            @classmethod
            def check_environment(cls, environ, config):

                """ Check for some import that this platform depends on. """

                try:
                    import cool_package
                except ImportError as e:
                    return False
                return True


    -- [property] `shortcut_exports`
        Accessed by apptools internals. Must be a structure in the format
        `list([tuple(<string>, <obj>)])`. Shortcuts exported in this way
        will appear on injected base classes as directly attached at the
        top-level of the object's dict. For example:

        Example:

            @property
            def shortcut_exports(self):

                """ Return exported base class shortcuts. """

                return [('api', self.api), ('my_cool_platform', self)]


        --- and then, many microseconds later in a handler far, far away ---


            class MyHandler(WebHandler):

                """ My cool injected handler. """

                def get(self):

                    """ HTTP GET """

                    self.api == MyPlatform.api


    -- [property] `template_context`
        Loaded by the AppTools output API to allow a Platform to inject data
        into the global Jinja2 template context. This is evaluated at runtime
        during the request processing flow, and thus has access to request
        environment data. Must return a closure to be executed during render,
        that accepts the parameters <handler> (the current handler) and
        <context> (the current Jinja2 context), the latter of which MUST be
        mutated in place and passed back.

        Example:

            @property
            def template_context(self):

                """ Return some local data that we have. """

                def inject_stuff(handler, context):

                    """ Inject `mycoolvar` into the Jinja2 template context. """

                    context['mycoolvar'] = 'wassup template!'
                    return context


        --- and then, many microseconds later in a template far, far away ---

            {% block injected %}
                {{ mycoolvar }}
            {% endblock injected %}


    -- [property] `config_shortcuts`
        Loaded and attached by the apptools internals to base classes in a very
        similar way to `shortcut_exports`. This structure, however, accepts
        a list of the form `list(tuple(<string>, <obj>))`, where <string> is a
        path to config. The resulting object is wrapped in a Webapp2 cached
        property and attached as a config shortcut.

        Mostly for internal use.


    -- [method] `pre_dispatch`(self, handler)
        Hook method that, if defined, is executed right before handler dispatch.
        The request flow can be stopped by raising an exception, but the return
        value of this function is ignored, so it's mostly for initialization.


    -- [method] `post_dispatch`(self, handler, response)
        Hook method that, if defined, is executed right after the response is
        returned from the handler. Once again, the request flow can be stopped
        via exceptions but the return value is ignored.


-sam (<sam.gammon@ampush.com>)

'''
