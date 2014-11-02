"""openbts.tests
tests for the package's primary modules
"""

import json
from multiprocessing import Process
import time
import unittest

import mock
import zmq

from openbts.components import OpenBTS
from openbts.core import BaseComponent
from openbts.exceptions import InvalidRequestError, TimeoutError


class BaseComponentTestCase(unittest.TestCase):
  """Testing the core.BaseComponent class.

  Contains a simple zmq server with a fixed response delay time that can be
  used to test socket timeout.  The idea is to run the demo server in another
  process.
  """
  # demo server will wait this many seconds before replying
  RESPONSE_DELAY = 0.2
  DEMO_ADDRESS = 'tcp://127.0.0.1:7890'

  def zmq_demo_server(self):
    """Run a small zmq testing server."""
    context = zmq.Context()
    server_socket = context.socket(zmq.REP)
    server_socket.bind(self.DEMO_ADDRESS)
    server_socket.recv()
    response = json.dumps({'code': 200, 'data': 'testing', 'dirty': 0})
    time.sleep(self.RESPONSE_DELAY)
    server_socket.send(response)

  def setUp(self):
    """Setup the zmq test server."""
    self.demo_server_process = Process(target=self.zmq_demo_server)
    self.demo_server_process.start()

  def tearDown(self):
    """Shutdown the demo zmq server."""
    self.demo_server_process.terminate()
    self.demo_server_process.join()

  def test_socket_timeout(self):
    """Base socket should raise a TimeoutError after receiving no reply."""
    component = BaseComponent(socket_timeout=self.RESPONSE_DELAY*0.9)
    component.socket.connect(self.DEMO_ADDRESS)
    with self.assertRaises(TimeoutError):
      component.read_config('sample-key')


class OpenBTSNominalConfigTestCase(unittest.TestCase):
  """Testing the openbts_component.OpenBTS class.

  Applying nominal uses of the 'config' command and 'openbts' target.
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

  def test_update_config_sends_message(self):
    """Updating a key should send a JSON-formatted message over zmq."""
    self.openbts_connection.update_config('sample-key', 'sample-value')
    self.assertTrue(self.openbts_connection.socket.send.called)
    expected_message = json.dumps({
      'command': 'config',
      'action': 'read',
      'key': 'sample-key',
      'value': 'sample-value'
    })
    self.assertEqual(self.openbts_connection.socket.send.call_args[0],
                     (expected_message,))

  def test_update_config_gets_response(self):
    """Updating a key should use the zmq socket and return a Response."""
    response = self.openbts_connection.update_config('sample-key',
                                                     'sample-value')
    self.assertTrue(self.openbts_connection.socket.recv.called)
    self.assertEqual(response.code, 204)


class OpenBTSOffNominalConfigTestCase(unittest.TestCase):
  """Testing the openbts_component.OpenBTS class.

  Examining off-nominal behaviors of the 'config' command and 'openbts' target.
  """
  def setUp(self):
    self.openbts_connection = OpenBTS()
    # mock a zmq socket with a simple recv return value
    self.openbts_connection.socket = mock.Mock()

  def test_read_config_unknown_key(self):
    """Reading a nonexistent key raises an error."""
    self.openbts_connection.socket.recv.return_value = json.dumps({
      'code': 404,
    })
    with self.assertRaises(InvalidRequestError):
      self.openbts_connection.read_config('nonexistent-key')

  def test_update_config_invalid_value(self):
    """Updating a value outside the allowed range raises an error."""
    self.openbts_connection.socket.recv.return_value = json.dumps({
      'code': 406,
    })
    with self.assertRaises(InvalidRequestError):
      self.openbts_connection.update_config('sample-key', 'sample-value')
