# -*- coding: utf-8 -*-

#
# DOCS COMING SOON :)
#

try:
	import uwsgi

except ImportError as e:
	## Not running in uWSGI.
	PLATFORM = 'WSGI'

else:
	PLATFORM = 'uWSGI'

def dispatch(environ, start_response):
	
	''' Regular WSGI Gateway '''

	start_response("200 OK", [("Content-Type", "text/html")])
	yield "<b>hello from python WSGI (HERMES)</b><br />"

	for k, v in environ.items():
		yield "<br /><b>%s:</b> %s" % (k, v)


def realtime(environ, start_response):
	
	''' Realtime WSGI Gateway '''

	uwsgi.websocket_handshake(env['HTTP_SEC_WEBSOCKET_KEY'], env.get('HTTP_ORIGIN', ''))
	while True:
		msg = uwsgi.websocket_recv()
		uwsgi.websocket_send(': '.join(['sup', msg]))

	return

