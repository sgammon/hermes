# -*- coding: utf-8 -*-

'''
Handlers for the API test harness, which provides a
clean sandbox and platform for testing API endpoints
and service methods.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.-sam (<sam.gammon@ampush.com>)
'''

# WebHandler
from api.handlers import WebHandler

# Core/Base Policy
from policy import core
from policy import base
from policy import click
from policy import conversion
from policy import impression

# Client/Custom Policy
from policy import clients
from policy.clients import *


## Sandbox - apptools JS sandbox
class Sandbox(WebHandler):

    ''' Playground for apptools JS. '''

    def get(self):

        ''' HTTP GET
            :returns: Rendered template ``harness/sandbox.html``. '''

        return self.render('harness/sandbox.html')


## Landing - testing harness landing page
class Landing(WebHandler):

    ''' Testing harness landing page. '''

    def get(self):

        ''' HTTP GET
            :returns: Rendered template ``harness/landing.html``. '''

        return self.render('harness/landing.html')
