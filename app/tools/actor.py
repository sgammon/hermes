# -*- coding: utf-8 -*-

"""
Tools: Actor Model

Allows a class to act as an `Actor`, which wakes up and processes
a singular type of task once new tasks are added via the internal
Gevent queue at `Actor.inbox`.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# gevent
import gevent
from gevent import queue


## Actor - manages an actor-model based engine
class Actor(gevent.Greenlet):

    ''' Individual Actor with queued processing functionality. '''

    inbox = None

    def initialize(self):

        ''' Initialize this actor. '''

        # Build a queue for an inbox of tasks
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

            # Block until we have a task, execute, then grab the next task...
            message = self.inbox.get()
            self.fire(message)
