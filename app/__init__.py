# -*- coding: utf-8 -*-

"""
Project: Hermes, by Ampush :)

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

## Package init for `Hermes.app`.
import bootstrap
from main import devserver
from main import APIServer

if __name__ == '__main__':
    devserver()  # if in doubt, run the devserver.
