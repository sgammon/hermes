# -*- coding: utf-8 -*-

'''
This package holds service middleware. Middleware classes export either (or both)
of the hook methods `before_request` and `after_request`, which will be picked up
and dispatched by the Service Layer. Register middleware classes in config at
`config.middleware.`

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# apptools services
try:
    from apptools import rpc
except:
    from apptools import services as rpc
