Getting Started
~~~~~~

Hermes is a Python-based platform designed from the ground up for building and supporting
latency-sensitive API services in a structured, flexible, and developer-friendly way.

By combining a rich application hosting environment, prebuilt base class structures,
integration with existing libraries, and a comprehensive dev toolchain, Hermes aims
to make the construction and deployment of enterprise-quality web services a breeze.


Server-Side
-------

Remotely-accessible `Services` group relevant methods, which are themselves bound to
datamodel-like structures called `Messages`. Think of a `Service` as a small WSGI
application, with your handlers or views being the methods contained within - except
you don't have to worry about parameters, paths, security, caching, serialization or HTTP.

Where you would regularly have a `Request`, you instead have a `Message`, which is fully
structured by you, The Developer. You can then (optionally) reply with your very own
`Message`, which is sent to the requesting party post-haste.

Let's take a look::

    # -*- coding: utf-8 -*-

    # apptools :) by momentum
    from apptools import model
    from apptools import services

    # hermes API services
    from api.services import APIService


    class Echo(model.Model):

        ''' A small message containing, well, a message. '''

        message = basestring, {'default': 'Hello, Hermes!'}


    @services.api(name='example')
    class ExampleService(APIService):

        ''' An example remote service for the docs. '''

        @services.rpcmethod(Echo)
        def echo(self, request):

            ''' Echo back what we get! '''

            return Echo(message=request.message)


That's it, you're done! Under the hood, `apptools` does some fancy metaclass stuff. Magically, your
service registers, loads, and is mounted to a new RPC endpoint (except if you don't want it to, if
you add `disabled=True` to the `services.api` decorator, in which case it is ignored in production).


Client-Side: JavaScript
--------

Once you have a service like the one above, the easiest way to call it is from `apptoolsJS` (**shocker**),
especially if you're in the JS context of a page served by apptools PY. You can achieve the same thing with
a static config object, too.

For instance, to dispatch the example above:

.. code-block:: js

    $.apptools.api.example.echo({message: "Hello from JavaScript!"}).fulfill({

        success: function (response) {  // this is our success callback
            console.log('Success! Got back:', response.message);
        },

        failure: function (error) {  // this is our failure callback
            console.error('Oh noez! Something failed.', error);
        }

    });


Woah! Where did that come from? Once you set up your server-side stuff, apptools PY injects the configuration
for your new service into the in-page configuration. When apptools JS picks it up again, it automatically
sets you up with a full set of stub-methods, namespaced under the `name` you provided to `@services.api` and
mounted at `$.apptools.api`.

The astute reader might also notice the reference to `response.message` - JSON serialization is performed
automatically, complete with built-in multiplexing and extensible transport support.


Client-Side: Python
-------

Hermes comes with tools to auto-generate structured client libraries from your server-side bindings. In the
`tools` directory, you'll find a script called `generate`. If you want, you can simply run it (but it will
also re-generate this documentation, build a **full** client library, and compile a bunch of stuff).

You can be a zen master and generate a Python library just for your service:

.. code-block:: console

   $ tools/generate py client --service example --endpoint "localhost:8080/v1/rpc"

   ========= Hermes: Compilation Routine =========

   --- Building client lib for service 'example'...

   building Python client...
   INFO:root:Writing package init at "tools/client/__init__.py".
   INFO:root:Writing package core to tools/client/core.py
   INFO:root:Writing package tracker to tools/client/example.py

   ========= Compilation succeeded. =========


Now that you've generated your client library, you can directly use it to query your service over HTTP!
To run this next one, you'll have to have your devserver running in another thread (or your example in
production, lols):

.. code-block:: pycon

   >>> import client, client.example as service
   >>> example = client.Client(service=service.ExampleService)  # build our client
   >>> print example.echo(message="Hello from Python!")
   <Echo message="Hello from Python!">

That's it! You'll also notice that if you assign the result of a `example.echo` to a local variable,
you can browse it like an object, because it **is an object**. So `response.message` works here, just
as it does in JavaScript.
