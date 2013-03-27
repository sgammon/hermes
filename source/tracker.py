# - coding: utf-8 -

# stdlib
import time

# gevent
import gevent
from gevent import pool
from gevent import local
from gevent import queue
from gevent import pywsgi
from gevent import monkey

# momentum libs
import webob
#import apptools
#import appfactory

# app-level code
from apps.hermes.source import exceptions

# protocol bindings
from apps.hermes.source import protocol
from apps.hermes.source.protocol import EventType
from apps.hermes.source.protocol import ParamConfig
from apps.hermes.source.protocol import EventProvider
from apps.hermes.source.protocol import ResponseStage
from apps.hermes.source.protocol import TrackerPrefix
from apps.hermes.source.protocol import TrackerProtocol


# Constants
debug = True		    # toggle debug mode
verbose = True		    # toggle verbose logging
_BLOCK_PDB = False          # PDB-stop immediately on __call__ - DANGEROUS, DO NOT USE IN PRODUCTION
_API_VERSION = "v1"         # prefix for tracking / API URLs
_TRACKER_MODE = "debug"     # advertised in `XAF-Tracker-Mode` response header
_TRACKER_VERSION = (0, 1)   # advertised in `XAF-Tracker-Version` response header
_TRACKER_RELEASE = "alpha"  # advertised in `XAF-Tracker-Version` response header
_PARAM_SEPARATOR = "_"      # seperator between prefix and param name
_DISCARD_NOSENTINEL = True  # refuse all incoming events missing a sentinel key
_REDIS_WRITE_POOL = 50      # perform up to X writes to redis concurrently

# Monkey-patch stdlib in debug (this is done for us in production by uWSGI)
if debug:
	monkey.patch_all()

# Provision locals and writepool
_locals = local.local()
_prebuffer = queue.Queue()
_writepool = pool.Pool(_REDIS_WRITE_POOL)


## InternalParams / AmpushParams - sets up prefix groups
InternalParams = frozenset([TrackerProtocol.DEBUG, TrackerProtocol.DRYRUN, TrackerProtocol.SENTINEL])
AmpushParams = frozenset([TrackerProtocol.REF, TrackerProtocol.TYPE, TrackerProtocol.CONTRACT, TrackerProtocol.SPEND, TrackerProtocol.PROVIDER])
AllParams = frozenset([getattr(TrackerProtocol, i) for i in TrackerProtocol.__dict__ if not i.startswith('_')])


## TrackedEvent - a conversion, impression, etc
class TrackedEvent(object):

	''' Represents a hit to a tracked event. '''

	id = None
	path = None
	params = {}
	request = None
	response = None
	match = None
	session = None
	cookie = None
	error = None
	sentinel = False
	tracker = None

	@classmethod
	def new(cls, tracker, request, response):

		''' Factory for a `TrackedEvent`. '''

		# Copy in request, path and params
		path, params = request.path, dict(request.params)
		return cls(tracker, request, params, response)

	def __init__(self, tracker, request, params, response):

		''' Initialize this `TrackedEvent`. '''

		# Initialize WSGI request/response properties
		self.tracker, self.request, self.path, self.params, self.response = tracker, request, request.path, params, response

                # Perform pre-validation
                if self.param(TrackerProtocol.SENTINEL) not in self.params:
			self.sentinel = False
                        if not _DISCARD_NOSENTINEL:
                                # Just warn if we're in debug...
                                self.tracker.warn("Not using the Sentinel value can cause bad counts. (Sentinel param is currently '%s'.)" % self.param(TrackerProtocol.SENTINEL))
                        else:
				self.tracker.error("No sentinel found, running in strict sentinel mode. (Sentinel param is currently '%s'.)" % self.param(TrackerProtocol.SENTINEL))
                                raise exceptions.InvalidSentinel("Sentinel key not found in tracker URL - event refused.")
		else:
			# Indicate we *do* have a sentinel
			self.tracker.verbose("Sentinel value found.")
			self.sentinel = True

		# Generate computed properties
		self.decode().generate_id(id(self))

	@property
	def debug(self):

		''' Indicate whether we're in debug mode (globally or per-request). '''

		return (debug or (self.param(TrackerProtocol.DEBUG) in params))

	def param(self, name):

		''' Get or set the value of a URL param. '''

		# If it's an Ampush param, add the prefix...
		if name in AmpushParams:
			param = _PARAM_SEPARATOR.join((TrackerPrefix.AMPUSH, name))

		# Same if it's an Internal param...
		elif name in InternalParams:
			param = _PARAM_SEPARATOR.join((TrackerPrefix.INTERNAL, name))

		# Otherwise, it's custom.
		else:
			param = _PARAM_SEPARATOR.join((TrackerPrefix.CUSTOM, name))

		self.tracker.verbose("Transformed param '%s' to '%s'." % (name, param))
		return param

	def generate_id(self, base):

		''' Generate a proper unique ID for this event. '''

		self.id = base
		return self

	def decode(self, injected=None):

		''' Decode an existing session, if any, or use `injected`. '''

		return self	

	def build(self, salt=None, pepper=None):

		''' Build a new local session, and return the new session ID. '''

		pass

	@property
	def session(self):

		''' Retrieve the current session object, or if there isn't one, build it anew. '''

		return "_SESSION_"

	@property
	def match(self):

		''' Retrieve any identified session matches. '''

		return self.seen()

	def generate_indexes(self):

		''' Generate index writes for a given `TrackedEvent`. '''

		pass

	def seen(self):

		''' Read Redis to see if we know this to be a match. '''

		return 'NONE'

	def put(self):

		''' Save this event to the Redis buffer. '''

		pass

	def __call__(self):

		''' Continue processing this event, once our background Greenlet/Thread picks up. '''

		time.sleep(2)
		return "cool"


## EventTracker
class EventTracker(object):

	''' WSGI-compliant application that tracks URL-dispatched events. '''

	# Base HTTP Details
        _base_headers = {
		'XAF-Tracker-Mode': 'DEBUG',
		'XAF-Tracker-Version': '-'.join(('.'.join(map(str, _TRACKER_VERSION)), _TRACKER_RELEASE))
        }.items()

	class BufferConfig(object):

		''' Static config class for `EventTracker`. '''

		frequency = 30   # empty the buffer every 30 seconds
		threshold = 100  # or every 100 events, whichever comes first

        params = None      # parameterset passed via the URL
	chunked = True     # indicate server-side support for chunked encoding
	session = None     # existing session cookie, if any
	prebuffer = None   # buffers according to the limits above
	lastflush = None   # holds a timestamp with the last flush
	flushqueue = None  # holds queued redis write greenlets

	def __init__(self):

		''' Initialize this `EventTracker`. '''

		self.lastflush = int(time.time())
		self.log("Debug mode is %s." % ("ON" if self.debug else "OFF"))
		self.log("Allocated writepool of size %s." % _REDIS_WRITE_POOL)

	@property
	def debug(self):

		''' Indicate whether we're in debug mode. '''

		return debug

	@property
	def prebuffer(self):

		''' Grab the global prebuffer. '''

		global _prebuffer
		return _prebuffer

	def _output(self, message, prefix=None):

		''' Low-level output pipe. '''

		if prefix:
			print "[%s] %s: %s" % ("TRACKER", prefix, message)
		else:
			print "[%s]: %s" % ("TRACKER", message)

	def log(self, message):

		''' Log something if we're in debug mode. '''

		if self.debug:
			self._output(message)
		return self

	def warn(self, message):

		''' Log a warning. '''

		self._output(message, "WARN")

	def error(self, message):

		''' Log an error. '''

		self._output(message, "ERROR")

	def verbose(self, message):

		''' Log something only if we're in debug AND verbose mode. '''

		if self.debug and verbose:
			self._output(message)
		return self

	def buffer(self, event):

		''' Add a `TrackedEvent` to the in-memory buffer. '''

		self.log("Sending event %s to prebuffer." % event.id)
		self.prebuffer.put_nowait(event)

		# See if the buffer needs to be flushed
		self.verbose("Checking buffer.")
		if self.check():
			self.flush()

		return id(event)

	def check(self):

		''' See if we need to close out the prebuffer. '''

		# We should flush if we've A) overflowed our soft buffer threshold or B) passed our flush timeout...
		timestamp = time.time()
		flush = ((self.prebuffer.qsize() > self.BufferConfig.threshold) or (self.lastflush + self.BufferConfig.frequency < timestamp))
		
		# Send logs
		did_timeout = "IS" if (self.lastflush + self.BufferConfig.frequency < timestamp) else "IS NOT"
		self.verbose("Current timestamp: %s." % timestamp)
		self.log("Buffer: Checkin-in at size %s with lastflush %s, which %s more than interval %s." % (self.prebuffer.qsize(), self.lastflush, did_timeout, self.BufferConfig.frequency))
		self.log("Flush %s recommended." % ("IS" if flush else "IS NOT"))
		
		return flush

	def flush(self):

		''' Flush the prebuffer to Redis. '''

		self.log("Buffer: Flushing %s events." % self.prebuffer.qsize())

        def begin_request(self, environ, start_response):

                ''' Factory a new `webob.Request`/`webob.Response` pair, representing a new HTTP transaction cycle. '''

                # Spawn request + response
                request, response = webob.Request(environ), webob.Response(content_type='text/html', charset='utf8')

		if verbose:
                        self.verbose("===== Request Environment =====")
                        self.verbose(str(environ))
			self.verbose("Provisioned WSGI request/response pair with IDs (%s, %s)." % (id(request), id(response)))
			self.verbose("Original response headers: \"%s\"." % response.headers)

                # Fill-in response info
		response.stage = ResponseStage.PENDING
                response.request = request
                for hkey, hvalue in self._base_headers:
                        response.headers[hkey] = hvalue

		if self.chunked:
			# Remove Content-Length for a chunked response
			self.verbose('Running in CHUNKED mode, removing Content-Length header.')
			del response.headers['Content-Length']

		self.verbose("Updated response headers: \"%s\"." % response.headers)
                return request, response

	def send_response(self, response, start_response, flush=False):

		''' Send the WSGI start_response call, optionally flushing the response buffer and finishing the transaction. '''

		self.verbose("Beginning response transmission.")
		if response.stage == ResponseStage.PENDING:
			# Send log messages
			self.log("Sending %s response with status \"%s\" and %s headers." % ("immediate" if flush else "deferred", response.status, len(response.headerlist)))
			self.verbose("Full response headers: \"%s\"." % response.headerlist)

			# Start response	        
		        start_response(response.status, response.headerlist)
			response.stage = ResponseStage.STARTED

		elif response.stage == ResponseStage.STARTED:
			# We've already started the response.
			self.log("Response already started, resuming deferred transaction.")

		if flush:
	                self.verbose("Flushing response body of length %s." % len(response.body))
			self.verbose("Full response body: \"%s\"." % response.app_iter)
			return response.body
		else:
			return response

	def __call__(self, environ, start_response):

		''' Handle a hit to a tracker URL. '''

		if debug and verbose and _BLOCK_PDB:
			import pdb; pdb.set_trace()

		# Spawn request + response
		request, response = self.begin_request(environ, start_response)
		self.log("Processing new request with ID %s." % id(request))

		try:
			# Factory new `TrackedEvent`.
			event = TrackedEvent.new(self, request, response)
			self.log("Spawned new `TrackedEvent` with ID %s." % event.id)

			# Begin building headers.
			response.headers['XAF-Match'] = event.match
			response.headers['XAF-Session'] = event.session

			self.log("Encountered match value %s with session %s." % (event.match, event.session))

		except exceptions.ClientError as e:

			# Handle 400-bound ClientError(s)
			response.status = 400
			response.body = '<b>Something terrible occurred, and it was <i>your</i> fault.</b>'
                        self.error("Encountered ClientError: \"%s\". Raising HTTP400." % e)

			body = self.send_response(response, start_response, flush=True)
			yield body
			raise StopIteration()

		except exceptions.PlatformError as e:

			# Handle 500-bound PlatformError(s)
			response.status = 500
			response.body = '<b>Oh noez, something broke.</b>'
			self.error("Encountered PlatformError: \"%s\". Raising HTTP500." % e)

			body = self.send_response(response, start_response, flush=True)
			yield body
			raise StopIteration()

		except exceptions.Error as e:

			# Handle 500-bound critical errors.
			self.error("Encountered known (but unhandled) exception: \"%s\"." % e)
			self.error("Exception description: \"%s\"." % e.__doc__)

			response.status = 500
			response.body = '<b>An unknown error occurred.</b>'
			body = self.send_response(response, start_response, flush=True)
			yield body
			raise  # re-raise after response
			raise StopIteration()

		try:
			self.verbose("Successfully provisioned new TrackedEvent. Starting deferred response.")

			# Start response with appropriate headers
			self.send_response(response, start_response, flush=False)

			# Buffer it and grab a simple ID to display
			self.verbose("Buffering event to write prebuffer.")
			buffer_id = self.buffer(event)

			response_buffer = []
				
			# Yield status message if debug mode is enabled.
			response_buffer.append(u"Event submitted with ID %s." % buffer_id)
			response_buffer.append(u"<b>Prebuffer size:</b> %s" % self.prebuffer.qsize())

		except Exception as e:
			raise  # re-raise core internal exceptions

		# We're done processing. Flush buffer and respond.
		self.log("Tracker transaction completed. Writing body.")
		self.verbose("Tracker response buffer of length %s:" % len(response_buffer))
		self.verbose(str(response_buffer))
		response.text = u"\n".join(response_buffer)

		response.stage = ResponseStage.COMPLETE
		self.verbose('Yielding to server-side transport.')
		for chunk in response.app_iter:
			yield chunk
		raise StopIteration()


## Spawn server singleton
EventTracker = EventTracker()

## Handle full-listener debug spawn
if __name__ == "__main__":
	# We're running this from the command line. Start an independent gevent server.
	server = pywsgi.WSGIServer(('', 8080), EventTracker)
	server.serve_forever()
	print "Closed."

