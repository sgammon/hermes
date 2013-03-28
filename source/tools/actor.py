# -*- coding: utf-8 -*-

# gevent
import gevent
from gevent import queue


## Actor - manages an actor-model based engine
class Actor(gevent.Greenlet):

	''' Individual Actor with queued processing functionality. '''

	def __init__(self):

		''' Initialize this actor. '''

		self.inbox = queue.Queue()
		gevent.Greenlet.__init__(self)

	def fire(self, message):

		''' Must be implemented by subclasses. '''

		raise NotImplemented()

	def _run(self):

		''' Run this ActorEngine and start processing items from the inbox. '''

		self.running = True
		while self.running:
			message = self.inbox.get()
			self.fire(message)
