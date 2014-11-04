"""integration testing
"""
import sys

import zmq

from openbts.components import OpenBTS, SMQueue, SIPAuthServe

if __name__ == '__main__':
  print ''
  print 'note: this script must be run against a live OpenBTS instance'
  print 'warning: during the test, this script will modify live config values'
  value = raw_input('\ncontinue? (y/n) ')
  if value.lower() != 'y':
    print 'exiting'
    sys.exit(1)
  print ''

  """ testing nominal config reads and updates
  """
  component_tests = [
    (OpenBTS, 'Control.NumSQLTries', '6'),
    (SIPAuthServe, 'Log.Alarms.Max', '12'),
    (SMQueue, 'Bounce.Code', 555)
  ]
  for entry in component_tests:
    print 'testing the %s:' % entry[0]()
    connection = entry[0]()
    response = connection.read_config(entry[1])
    original_value = response.data['value']
    print '  original value of %s: %s' % (entry[1], original_value)
    connection.update_config(entry[1], entry[2])
    response = connection.read_config(entry[1])
    print '  set %s to %s' % (entry[1], entry[2])
    connection.update_config(entry[1], original_value)
    response = connection.read_config(entry[1])
    print '  reverted %s to %s' % (entry[1], response.data['value'])
    print ''

  """ testing nominal OpenBTS monitoring
  """
  print 'getting OpenBTS monitoring data:'
  connection = OpenBTS()
  response = connection.monitor()
  print '  noise RSSI: %s' % response.data['noiseRSSI']
  print ''

  print '\nintegration test complete.'
  print ''
