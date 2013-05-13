# -*- coding: utf-8 -*-

import sys, os

ROOT_PATH = '/'.join(os.path.abspath(__file__).split('/')[0:-2])
APP_PATH = '/'.join([ROOT_PATH, 'app'])
LIB_PATH = '/'.join([APP_PATH, 'lib'])
DISTLIB_PATH = '/'.join([LIB_PATH, 'dist'])

for x in (ROOT_PATH, APP_PATH, LIB_PATH, DISTLIB_PATH):
    if x not in sys.path:
        sys.path = [x] + sys.path

import bootstrap
