# -*- coding: utf-8 -*-

"""
Hermes: Tools

This package contains low-level tools for Hermes-specific datastructures
and design patterns. Most notable is the `Actor` greenlet pattern, which
is used in the `DatastoreEngine` component of the `EventTracker`.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# Actor Model
from . import actor
from .actor import Actor


__all__ = [actor, Actor]
