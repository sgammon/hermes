#!/usr/bin/env python
#
# Copyright 2011 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Command line tool for generating ProtoRPC definitions from descriptors."""

import errno
import logging
import optparse
import os
import sys

from tools.internal import generate_python
from protorpc import descriptor
from protorpc import protobuf
from protorpc import generate
from protorpc import registry
from protorpc import transport
from protorpc import util

EXCLUDED_PACKAGES = frozenset(['protorpc.registry',
                               'protorpc.messages',
                               'protorpc.descriptor',
                               'protorpc.message_types',
                               ])

commands = {}
_written_package_roots = set()


def usage():
  """Print usage help and exit with an error code."""
  parser.print_help()
  sys.exit(2)


def fatal_error(message):
  """Print fatal error messages exit with an error code.

  Args:
    message: Message to print to stderr before exit.
  """
  sys.stderr.write(message)
  sys.exit(1)


def open_input_file(filename):
  """Open file for reading.

  Args:
    filename: Name of input file to open or None to open stdin.

  Returns:
    Opened file if string provided, stdin if filename is None.
  """
  # TODO(rafek): Detect missing or invalid files, generating user friendly
  # error messages.
  if filename is None:
    return sys.stdin
  else:
    try:
      return open(filename, 'rb')
    except IOError, err:
      fatal_error(str(err))


def mutate_field(descriptor):

  ''' Mutate a message field for use in a client package. '''

  # check typename path
  if descriptor.type_name and descriptor.type_name.startswith('apptools.model.adapter.protorpc'):
    descriptor.type_name = '.'.join(['client.core', descriptor.type_name.split('.')[-1]])

  # manually quote strings, because google doesn't escape them properly (WTF GOOGLE?? WHY U NO QUOTE.)
  if descriptor.default_value and isinstance(descriptor.default_value, basestring):
    descriptor.default_value = "'%s'" % descriptor.default_value  # crazy damn hax.

  return descriptor


def mutate_message(descriptor):

  ''' Mutate a message for use in a client package. '''

  if descriptor.name == 'Message':
    return None  # don't dump `Message`
  fields = []
  for field in descriptor.fields:
    f = mutate_field(field)
    if f:
      fields.append(f)

  descriptor.fields = fields
  return descriptor


def mutate_method(descriptor):

  ''' Mutate a service method for use in a client package. '''

  # filter `request_type`
  if descriptor.request_type.startswith('api.services'):
    spl = descriptor.request_type.split('.')
    if spl[-2] != 'service':
      prefix = spl[-2]
    else:
      prefix = spl[-3]
    descriptor.request_type = '.'.join(['%s' % prefix, spl[-1]])

  elif descriptor.request_type.startswith('apptools.model.adapter.protorpc'):
    descriptor.request_type = '.'.join(['core', descriptor.request_type.split('.')[-1]])

  # filter `response_type`
  if descriptor.response_type.startswith('api.services'):
    spl = descriptor.response_type.split('.')
    if spl[-2] != 'service':
      prefix = spl[-2]
    else:
      prefix = spl[-3]
    descriptor.response_type = '.'.join(['%s' % prefix, spl[-1]])

  elif descriptor.response_type.startswith('apptools.model.adapter.protorpc'):
    descriptor.response_type = '.'.join(['core', descriptor.response_type.split('.')[-1]])

  return descriptor


def mutate_service(descriptor):

  ''' Mutate a service for use in a client package. '''

  if descriptor.name == 'APIService':
    return None  # don't factory APIService - it's an abstract class

  methods = []
  for method in descriptor.methods:
    m = mutate_method(method)
    if m:
      methods.append(m)

  descriptor.methods = methods
  return descriptor


def mutate_descriptor(descriptor):

  ''' Used by Ampush/Apptools-based code to generate custom Python clients. '''

  services, messages = [], []
  if descriptor.package.startswith('api.services'):

    # change origin package to client
    spl = descriptor.package.split('.')[2:-1]
    descriptor.package = '.'.join(spl)

  if descriptor.package.startswith('apptools.model'):

    # change origin package to client core
    descriptor.package = '.'.join(['core'] + descriptor.package.split('.')[4:])

  # give message mutator a chance to change/filter messages
  for mutator, bundle, target in ((mutate_message, descriptor.message_types, messages), (mutate_service, descriptor.service_types, services)):
    for source in bundle:
      m = mutator(source)
      if m:
        target.append(m)

  descriptor.message_types = messages
  descriptor.service_types = services

  return descriptor


@util.positional(1)
def generate_file_descriptor(dest_dir, file_descriptor, force_overwrite, indent_space=2):
  """Generate a single file descriptor to destination directory.

  Will generate a single Python file from a file descriptor under dest_dir.
  The sub-directory where the file is generated is determined by the package
  name of descriptor.

  Descriptors without package names will not be generated.

  Descriptors that are part of the ProtoRPC distribution will not be generated.

  Args:
    dest_dir: Directory under which to generate files.
    file_descriptor: FileDescriptor instance to generate source code from.
    force_overwrite: If True, existing files will be overwritten.
  """

  file_descriptor = mutate_descriptor(file_descriptor)

  package = file_descriptor.package
  if not package:
    # TODO(rafek): Option to cause an error on this condition.
    logging.warn('Will not generate descriptor without package name')
    return

  if package in EXCLUDED_PACKAGES:
    logging.warn('Will not generate main ProtoRPC class %s' % package)
    return

  package_path = package.split('.')
  directory = package_path[:-1]
  package_file_name = package_path[-1]
  directory_name = os.path.join(dest_dir, *directory)
  output_file_name = os.path.join(directory_name,
                                  '%s.py' % (package_file_name,))

  try:
    os.makedirs(directory_name)
  except OSError, err:
    if err.errno != errno.EEXIST:
      raise

  output_file = open(output_file_name, 'w')

  # make package `__init__`
  package_init = '/'.join([directory_name, '__init__.py'])
  if package_init not in _written_package_roots:
    init_fd = open(package_init, 'w')
    init = generate.IndentWriter(init_fd, indent_space=indent_space)
    init << '# -*- coding: utf-8 -*-'
    init << '# Client init.'
    _written_package_roots.add(package_init)
    logging.info('Writing package init at "%s".' % package_init)
    init_fd.close()

  if not force_overwrite and os.path.exists(output_file_name):
    logging.warn('Not overwriting %s with package %s',
                 output_file_name, package)
    return

  logging.info('Writing package %s to %s',
               file_descriptor.package, output_file_name)
  generate_python.format_python_file(file_descriptor, output_file)  # pass-through to client mutator


@util.positional(1)
def command(name, required=(), optional=()):
  """Decorator used for declaring commands used on command line.

  Each command of this tool can have any number of sequential required
  parameters and optional parameters.  The required and optional parameters
  will be displayed in the command usage.  Arguments passed in to the command
  are checked to ensure they have at least the required parameters and not
  too many parameters beyond the optional ones.  When there are not enough
  or too few parameters the usage message is generated and the program exits
  with an error code.

  Functions decorated thus are added to commands by their name.

  Resulting decorated functions will have required and optional attributes
  assigned to them so that appear in the usage message.

  Args:
    name: Name of command that will follow the program name on the command line.
    required: List of required parameter names as displayed in the usage
      message.
    optional: List of optional parameter names as displayed in the usage
      message.
  """
  def check_params_decorator(function):
    def check_params_wrapper(options, *args):
      if not (len(required) <= len(args) <= len(required) + len(optional)):
        sys.stderr.write("Incorrect usage for command '%s'\n\n" % name)
        usage()
      function(options, *args)
    check_params_wrapper.required = required
    check_params_wrapper.optional = optional
    commands[name] = check_params_wrapper
    return check_params_wrapper
  return check_params_decorator


@command('file', optional=['input-filename', 'output-filename'])
def file_command(options, input_filename=None, output_filename=None):
  """Generate a single descriptor file to Python.

  Args:
    options: Parsed command line options.
    input_filename: File to read protobuf FileDescriptor from.  If None
      will read from stdin.
    output_filename: File to write Python source code to.  If None will
      generate to stdout.
  """
  with open_input_file(input_filename) as input_file:
    descriptor_content = input_file.read()

  if output_filename:
    output_file = open(output_filename, 'w')
  else:
    output_file = sys.stdout

  file_descriptor = protobuf.decode_message(descriptor.FileDescriptor,
                                            descriptor_content)
  generate_python.format_python_file(file_descriptor, output_file)


@command('fileset', optional=['filename'])
def fileset_command(options, input_filename=None):
  """Generate source directory structure from FileSet.

  Args:
    options: Parsed command line options.
    input_filename: File to read protobuf FileSet from.  If None will read from
      stdin.
  """
  with open_input_file(input_filename) as input_file:
    descriptor_content = input_file.read()

  dest_dir = os.path.expanduser(options.dest_dir)

  if not os.path.isdir(dest_dir) and os.path.exists(dest_dir):
    fatal_error("Destination '%s' is not a directory" % dest_dir)

  file_set = protobuf.decode_message(descriptor.FileSet,
                                     descriptor_content)

  for file_descriptor in file_set.files:
    generate_file_descriptor(dest_dir, file_descriptor=file_descriptor,
                             force_overwrite=options.force)


@command('registry',
         required=['host'],
         optional=['service-name', 'registry-path'])
def registry_command(options,
                     host,
                     service_name=None,
                     registry_path='/protorpc'):
  """Generate source directory structure from remote registry service.

  Args:
    options: Parsed command line options.
    host: Web service host where registry service is located.  May include
      port.
    service_name: Name of specific service to read.  Will generate only Python
      files that service is dependent on.  If None, will generate source code
      for all services known by the registry.
    registry_path: Path to find registry if not the default 'protorpc'.
  """
  dest_dir = os.path.expanduser(options.dest_dir)

  from apptools.services import mappers

  url = 'http://%s%s' % (host, registry_path)
  reg = registry.RegistryService.Stub(transport.HttpTransport(url, protocol=mappers.JSONRPCMapper))

  if service_name is None:
    service_names = [service.name for service in reg.services().services]
  else:
    service_names = [service_name]

  file_set = reg.get_file_set(names=service_names).file_set

  import pdb; pdb.set_trace()
  for file_descriptor in file_set.files:
    generate_file_descriptor(dest_dir, file_descriptor=file_descriptor,
                             force_overwrite=options.force)


def make_opt_parser():
  """Create options parser with automatically generated command help.

  Will iterate over all functions in commands and generate an appropriate
  usage message for them with all their required and optional parameters.
  """
  command_descriptions = []
  for name in sorted(commands.iterkeys()):
    command = commands[name]
    params = ' '.join(['<%s>' % param for param in command.required] +
                      ['[<%s>]' % param for param in command.optional])
    command_descriptions.append('%%prog [options] %s %s' % (name, params))
  command_usage = 'usage: %s\n' % '\n       '.join(command_descriptions)

  parser = optparse.OptionParser(usage=command_usage)
  parser.add_option('-d', '--dest_dir',
                    dest='dest_dir',
                    default=os.getcwd(),
                    help='Write generated files to DIR',
                    metavar='DIR')
  parser.add_option('-f', '--force',
                    action='store_true',
                    dest='force',
                    default=False,
                    help='Force overwrite of existing files')
  return parser

parser = make_opt_parser()


def main():
  # TODO(rafek): Customize verbosity.
  logging.basicConfig(level=logging.INFO)
  options, positional = parser.parse_args()

  if not positional:
    usage()

  command_name = positional[0]
  command = commands.get(command_name)
  if not command:
    sys.stderr.write("Unknown command '%s'\n\n" % command_name)
    usage()
  parameters = positional[1:]

  command(options, *parameters)


if __name__ == '__main__':
  main()
