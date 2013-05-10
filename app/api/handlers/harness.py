# -*- coding: utf-8 -*-

'''

API Handlers: Harness

Handlers for the API test harness.

-sam (<sam.gammon@ampush.com>)

'''

# stdlib
import os
import sys

# WebHandler
from api.handlers import WebHandler


## SandboxHandler - apptools JS sandbox
class SandboxHandler(WebHandler):

    ''' Playground for apptools JS. '''

    def get(self):

        ''' HTTP GET '''

        return self.render('harness/sandbox.html')
