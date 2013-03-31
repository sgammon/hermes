# -*- coding: utf-8 -*-

# WebHandler
from api.handlers import WebHandler


## TestHandler - test apptools
class TestHandler(WebHandler):

	''' Test AppTools handler functionality. '''

	def get(self):

		''' HTTP GET '''

		return '<html><head><title>sup</title></head><body><b>sup</b></body></html>'
