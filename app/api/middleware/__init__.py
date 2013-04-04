# -*- coding: utf-8 -*-

'''

API: Middleware

This package holds service middleware. Middleware classes export either (or both)
of the hook methods `before_request` and `after_request`, which will be picked up
and dispatched by the Service Layer. Register middleware classes in config at
`config.middleware.`

-sam (<sam.gammon@ampush.com>)

'''
