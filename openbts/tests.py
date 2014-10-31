"""openbts.tests
tests for the package's primary modules
"""

import json
import mock
import unittest

from openbts.openbts_component import OpenBTS


class OpenBTSNominalConfigTestCase(unittest.TestCase):
  """Testing the openbts_component.OpenBTS class.

  Testing nominal uses of the 'config' command and 'openbts' target.
  """

  def setUp(self):
    self.openbts_connection = OpenBTS()
    # mock a zmq socket with a simple recv return value
    self.openbts_connection.socket = mock.Mock()
    self.openbts_connection.socket.recv.return_value = json.dumps({
      'code': 204,
      'data': 'sample',
      'dirty': 0
    })

  def test_read_config_sends_message(self):
    """Reading a key should send a JSON-formatted message over zmq."""
    self.openbts_connection.read_config('sample-key')
    self.assertTrue(self.openbts_connection.socket.send.called)
    expected_message = json.dumps({
      'command': 'config',
      'action': 'read',
      'key': 'sample-key',
      'value': ''
    })
    self.assertEqual(self.openbts_connection.socket.send.call_args[0],
                     (expected_message,))

  def test_read_config_gets_response(self):
    """Reading a key should use the zmq socket and return a Response."""
    response = self.openbts_connection.read_config('sample-key')
    self.assertTrue(self.openbts_connection.socket.recv.called)
    self.assertEqual(response.code, 204)
