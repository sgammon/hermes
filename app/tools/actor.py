# -*- coding: utf-8 -*-

'''

Tools: Actor Model

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''

# gevent
import gevent
from gevent import queue


## Actor - manages an actor-model based engine
class Actor(gevent.Greenlet):

	''' Individual Actor with queued processing functionality. '''

	inbox = None

	def initialize(self):

		''' Initialize this actor. '''

		self.inbox = queue.Queue()
		gevent.Greenlet.__init__(self)
		return self

	def fire(self, message):

		''' Must be implemented by subclasses. '''

		raise NotImplemented()

	def _run(self):

		''' Run this ActorEngine and start processing items from the inbox. '''

		self.running = True
		while self.running:
			message = self.inbox.get()
			self.fire(message)
