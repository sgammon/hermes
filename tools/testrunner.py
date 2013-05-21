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


def main(test_path='app', mode='text', output='../.tests'):  # pragma: no cover

    sys.path.append('.')
    sys.path.append(test_path)
    sys.path.append('/'.join([test_path, 'lib']))
    sys.path.append('/'.join([test_path, 'lib', 'dist']))

    import bootstrap
    bootstrap.AppBootstrapper.prepareImports()

    from apptools import tests

    loader = unittest.loader.TestLoader()
    suites, suite = [], unittest.TestSuite()

    for directory in ('app/', 'app/api/', 'app/tools/', 'app/util'):

        # Discovery patterns
        for pattern in frozenset(['tests',
                                  'tests/**',
                                  '*.py',
                                  '**/*.py',
                                  'test_*.py']):
            try:
                suites.append(loader.discover(str(directory), pattern=pattern))
            except TypeError:
                print "Could not add directory '%s' with pattern '%s'." % (directory, pattern)
                continue
            else:
                continue

    # Add AppTools
    suites.append(tests.load())

    # Add top-level discover
    suites.append(loader.discover(test_path))
    suites.append(loader.loadTestsFromTestCase(tests.AppTest))

    # filter out dupes
    alltests = []
    for suite in suites:
        for test in suite:
            if test not in alltests:
                alltests.append(test)

    # Compile into a suite...
    suite.addTests(unittest.TestSuite(alltests))
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
