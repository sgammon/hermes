# -*- utf-8 -*-

'''

API: Init

Ampush Hermes is an API platform for efficiently exposing RPCAPI services
and performing other down-and-dirty backend tasks. Thus, as an app, it is
simply called "api". :)

The codebase is organized a lot like a regular apptools app, so it's got
the standard directories:

	-- handlers/
	   Contains RequestHandler-descendent classes that are bound to
	   one-or-many URLs and are responsible for handling a single
	   HTTP request/response lifecycle. All you have to do to make
	   one is extend `handlers.WebHandler` and define your HTTP
	   methods as, well... methods.

	   For example:

	   		from handlers import WebHandler

	   		class MyCoolHandler(WebHandler):

	   			""" Hey look I'm a handler """

	   			def get(self):

	   				""" Called upon HTTP GET """

	   				return self.render("cool/template.html")  # render a template, why not


	-- messages/
	   This directory holds structured message classes that express
	   request or response datastructures for the apptools service
	   layer. Since apptools models can be used transparently as
	   messages, only explicitly-defined or custom-built message
	   classes need to live here. These are directly ProtoRPC-
	   descendent message classes, so refer to that documentation for
	   writing your own.

	   For example:

	   		from protorpc import messages

	   		class Person(messages.Message):

	   			""" We can use this as a request or response message. """

	   			firstname = messages.StringField(1)
	   			lastname = messages.StringField(2, required=True)
	   			age = messages.IntegerField(3)


	-- middleware/
	   This directory contains service layer middleware classes, which
	   hook into the request/response flow for an API dispatch lifecycle
	   and have a chance at doing something *before* or *after* the
	   request. Middleware classes must be registered in config to be
	   autoloaded by apptools.


	-- models/
	   Put your datamodels here! This is where all datamodels go, to
	   hopefully try and mitigate circular dependencies.


	-- platform/
	   AppTools Platforms deserve a description all their own - and they
	   have one, in platform/__init__ :). Essentially, a platform is
	   where you put code that has a responsibility spanning multiple
	   app base classes - for instance, code that needs to be dispatched
	   from a handler *and* a service, but *must* not be duplicated.


	-- services/
	   AppTools service classes live here. Services are responsible for
	   responding to API requests, and are integrated tightly with
	   AppTools JS and Google Cloud Endpoints, if running on App Engine.
	   Services structure requests and responses via `messages` (see
	   above) and can inject functionality before or after dispatch by
	   utilizing `middleware` (also see above).


	-- templates/
	   Jinja2 template root. Put your source HTML into `templates/source`.
	   The prefix for templates is set at runtime, depending on whether
	   the current environment supports compiled templates, they are up-
	   to-date, and you have selected to enable them via config.


	-- tests/
	   Of course, this is where unit and integration tests live. There can
	   never be enough tests and if your criticism starts there, I've done
	   my job! :)


-sam (<sam.gammon@ampush.com>)

'''
