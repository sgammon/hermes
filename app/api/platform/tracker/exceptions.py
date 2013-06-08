# -*- coding: utf-8 -*-

'''
API: Exceptions

Top-level exceptions are defined here, including Hermes'
package-level catchall, defined as `Error`.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# top-level exceptions
from api import exceptions


# TrackerPlatformException - top-level abstract exception for all `platform`-related exceptions.
class TrackerPlatformException(exceptions.CorePlatformException): pass


# TrackerEngineException - parent exception for problems in the `platform`-proper.
class TrackerEngineException(TrackerPlatformException): pass


# EngineSubsystemException - parent exception for problems in `platform` subsystems.
class EngineSubsystemException(TrackerEngineException): pass


# PolicyEngineException - parent exception for problems in the ``PolicyEngine`` subsystem.
class PolicyEngineException(EngineSubsystemException): pass


# CorePolicyException - indicates problems processing or interpreting policy.
class CorePolicyException(PolicyEngineException): pass


# ParamsetException - indicates problems interpreting or applying a ``paramset``.
class ParamsetException(CorePolicyException): pass


# InvalidParamName - indicates that a param name is invalid.
class InvalidParamName(ParamsetException): pass


# MissingParameter - raised when an expected parameter was not found.
class MissingParameter(ParamsetException): pass


# UnexpectedParameter - raised when an unexpected parameter was found.
class UnexpectedParameter(ParamsetException): pass


# InvalidParameterValue - raised when type conversion fails for a param value.
class InvalidParameterValue(ParamsetException): pass
