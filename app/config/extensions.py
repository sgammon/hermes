# -*- coding: utf-8 -*-

"""
Config: Extensions

This file holds config for extensions to the AppTools Output API.
Jinja2 extensions are also valid Output API extensions.

:author: Sam Gammon (sam.gammon@ampush.com)
:copyright: (c) 2013 Ampush.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

"""

    ######################################## output extension configuration. ########################################

"""

config = {}

## DynamicContent extension - manages injection of dynamic, editable content into template AST's
config['apptools.output.extension.DynamicContent'] = {

    'debug': True,
    'enabled': True,
    'logging': False,

    'config': {
        'default_namespace': '::'.join(['amp', 'tpl', 'dynamic', 'system'])
    }

}

## FragmentCache extension - makes caching possible in the template via a {% cache %} tag
config['apptools.output.extension.FragmentCache'] = {

    'debug': True,
    'enabled': True,
    'logging': False,

    'config': {
        'timeout': 1200,  # default timeout of 5 minutes
        'prefix': '::'.join(['amp', 'tpl', 'source', 'fragment'])
    }

}

## ThreadedBytecodeCache extension - caches compiled template bytecode in thread memory
config['apptools.output.extension.ThreadedBytecodeCache'] = {

    'debug': True,
    'enabled': True,
    'logging': False,

    'config': {
        'timeout': 1200,  # default timeout of 5 minutes
        'prefix': '::'.join(['amp', 'tpl', 'bytecode', 'tcache'])
    }

}

## MemcachedBytecodeCache extension - caches compiled template bytecode in memcache
config['apptools.output.extension.MemcachedBytecodeCache'] = {

    'debug': True,
    'enabled': True,
    'logging': False,

    'config': {
        'timeout': 1200,
        'prefix': '::'.join(['amp', 'tpl', 'bytecode', 'mcache'])
    }

}
