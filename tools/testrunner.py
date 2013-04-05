#!/usr/bin/python
# -*- coding: utf-8 -*-

'''

Hermes: Testrunner

Description coming soon.

-sam (<sam.gammon@ampush.com>)

'''


import sys
import optparse
import unittest
import xmlrunner

USAGE = """%prog SDK_PATH TEST_PATH
Run unit tests for AppFactory apps.

TEST_PATH   Path to package containing test modules"""


def main(test_path='app/', mode='text', output='../.tests'):

    from apptools import tests

    loader = unittest.loader.TestLoader()
    suites, suite = [], unittest.TestSuite()

    sys.path.append('.')
    sys.path.append(test_path)

    import bootstrap
    bootstrap.AppBootstrapper.prepareImports()


    for directory in ('app/', 'app/api/', 'app/components/', 'app/tools/', 'app/util'):

        # Discovery patterns
        suites.append(loader.discover(directory, pattern='tests'))
        suites.append(loader.discover(directory, pattern='tests/**'))
        suites.append(loader.discover(directory, pattern='*.py'))
        suites.append(loader.discover(directory, pattern='**/*.py'))
        suites.append(loader.discover(directory, pattern='test_*.py'))

    # Add AppTools
    suites.append(tests.AppToolsTests)

    # Add top-level discover
    suites.append(loader.discover(test_path))
    suites.append(loader.loadTestsFromTestCase(tests.AppTest))

    # Compile into a suite...
    suite.addTests(suites)
    if mode == 'text':
        unittest.TextTestRunner(verbosity=5).run(suite)
    elif mode == 'xml':
        xmlrunner.XMLTestRunner(output=output).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    if len(args) == 4:
        SDK_PATH, TEST_PATH, MODE, OUTPUT = tuple(args)
        main(SDK_PATH, TEST_PATH, MODE, OUTPUT)
    elif len(args) == 3:
        SDK_PATH, TEST_PATH, MODE = tuple(args)
        main(SDK_PATH, TEST_PATH, MODE)
    elif len(args) == 2:
        TEST_PATH, MODE = tuple(args)
        main(test_path=TEST_PATH, mode=MODE)
    elif len(args) == 1:
        TEST_PATH = args[0]
        main(test_path=TEST_PATH)
    elif not args:
        main()
