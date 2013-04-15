# -*- coding: utf-8 -*-

'''

API: Test Handlers

Handlers that test functionality in Hermes or Apptools itself.

-sam (<sam.gammon@ampush.com>)

'''

# stdlib
import os
import sys

# WebHandler
from api.handlers import WebHandler


## TestHandler - test apptools
class TestHandler(WebHandler):

    ''' Test AppTools handler functionality. '''

    def get(self, mode='hello'):

        ''' HTTP GET '''

        if mode == 'env':
            return self.render('test/env.html', request=self.request, environ=os.environ, sysflags=sys.flags, handler=self)
        return self.render('test/hello.html')
