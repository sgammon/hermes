# -*- coding: utf-8 -*-

'''

Hermes: Tools

This package contains low-level tools for Hermes-specific datastructures
and design patterns. Most notable is the `Actor` greenlet pattern, which
is used in the `DatastoreEngine` component of the `EventTracker`.

-sam (<sam.gammon@ampush.com>)

'''

# Actor Model
from . import actor
from .actor import Actor


__all__ = [actor, Actor]
