"""integration testing
"""
import sys

import zmq

from openbts.components import OpenBTS
from openbts.exceptions import InvalidRequestError

if __name__ == '__main__':
  print 'note: this script must be run against a live OpenBTS instance'
  print 'warning: during the test, this script will modify live config values'
  value = raw_input('\ncontinue? (y/n) ')
  if value.lower() != 'y':
    sys.exit(1)

  print 'testing the OpenBTS component'
  openbts_connection = OpenBTS()

  """ read - update - read
  """
  path = 'Control.NumSQLTries'
  # TODO(matt): do we always send strings?
  update_value = '3'
  print 'reading "%s"' % path
  response = openbts_connection.read_config(path)
  print '  value: %s' % response.data['value']
  print 'updating "%s" to "%s"' % (path, update_value)
  response = openbts_connection.update_config(path, update_value)
  print '  response code: %s' % response.code
  print 'reading "%s"' % path
  response = openbts_connection.read_config(path)
  print '  value: %s' % response.data['value']
