# -*- coding: utf-8 -*-

'''

API: Templates

This directory stores HTML templates for use with Jinja2 and the AppTools
Output API. Raw HTML source is kept in `source/`, and compiled Python code
from that source is kept in `compiled/`.

AppTools ships with a script called `compile_templates` which will run the
Jinja2 compiler over your source HTML and generate compiled versions. The
AppTools distro of Jinja2 is patched (courtesy of Rodrigo Moraes, the master
himself) to enable export of an environment render function, meaning compiled
template code can be cached as imports.

This makes templates *very* fast. It is *highly* recommended.

The standard AppTools cakefile ships with a command to compile the templates
for you, if your app layout is standard and supports such a thing. In that
case, you can simply execute `cake compile:templates` to compile, and
`cake clean:templates` to clean existing compiled code.

Notable template directories:

	-- source/core
	   Contains base templates, including the root (__base.html).

	-- source/macros
	   Contains built-in and custom importable macros for various things.

	-- source/*
	   App templates! :)


-sam (<sam.gammon@ampush.com>)

'''
