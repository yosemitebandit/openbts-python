"""openbts.tests
tests for the package's primary modules
"""

import json
from multiprocessing import Process
import time
import unittest

import mock
import zmq

from openbts.components import OpenBTS, SIPAuthServe
from openbts.core import BaseComponent
from openbts.exceptions import InvalidRequestError, TimeoutError


class BaseComponentTestCase(unittest.TestCase):
  """Testing the core.BaseComponent class.

  Contains a simple zmq server with a fixed latency.  The simulated latency
  allows us to test socket timeout features.  The idea is to run the demo
  server in another process and then connect through a test client.
  """
  # demo server will wait this many seconds before replying
  RESPONSE_DELAY = 0.1
  DEMO_ADDRESS = 'tcp://127.0.0.1:7890'

  def zmq_demo_server(self):
    """Run a small zmq testing server."""
    context = zmq.Context()
    server_socket = context.socket(zmq.REP)
    server_socket.bind(self.DEMO_ADDRESS)
    server_socket.recv()
    response = json.dumps({'code': 200, 'data': 'testing', 'dirty': 0})
    # delay a bit before sending the reply
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
    # server will delay before sending response
    # so we set the timeout to be a bit less than that amount
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

  def test_create_config_raises_error(self):
    """Creating a config key should is not yet supported via NodeManager."""
    with self.assertRaises(InvalidRequestError):
      self.openbts_connection.create_config('sample-key', 'sample-value')

  def test_read_config_sends_message_and_receives_response(self):
    """Reading a key should send a message over zmq and get a response."""
    response = self.openbts_connection.read_config('sample-key')
    # check that we touched the socket to send the message
    self.assertTrue(self.openbts_connection.socket.send.called)
    expected_message = json.dumps({
      'command': 'config',
      'action': 'read',
      'key': 'sample-key',
      'value': ''
    })
    # check that we've sent the expected message
    self.assertEqual(self.openbts_connection.socket.send.call_args[0],
                     (expected_message,))
    # we should have touched the socket again to receive the reply
    self.assertTrue(self.openbts_connection.socket.recv.called)
    # verify we received a valid response
    self.assertEqual(response.code, 204)

  def test_update_config_sends_message_and_receives_response(self):
    """Updating a key should send a message over zmq and get a response."""
    response = self.openbts_connection.update_config('sample-key',
                                                     'sample-value')
    self.assertTrue(self.openbts_connection.socket.send.called)
    expected_message = json.dumps({
      'command': 'config',
      'action': 'update',
      'key': 'sample-key',
      'value': 'sample-value'
    })
    self.assertEqual(self.openbts_connection.socket.send.call_args[0],
                     (expected_message,))
    self.assertTrue(self.openbts_connection.socket.recv.called)
    self.assertEqual(response.code, 204)

  def test_delete_config_raises_error(self):
    """Deleting a config key should is not yet supported via NodeManager."""
    with self.assertRaises(InvalidRequestError):
      self.openbts_connection.delete_config('sample-key')

  def test_responses_with_no_dirty_param_parsed_successfully(self):
    """We should handle responses that don't have the 'dirty' attribute."""
    self.openbts_connection.socket.recv.return_value = json.dumps({
      'code': 200,
      'data': 'sample'
    })
    response = self.openbts_connection.read_config('sample-key')
    self.assertEqual(response.code, 200)

  def test_responses_with_no_data_param_parsed_successfully(self):
    """We should handle responses that don't have the 'data' attribute."""
    self.openbts_connection.socket.recv.return_value = json.dumps({
      'code': 200,
    })
    response = self.openbts_connection.read_config('sample-key')
    self.assertEqual(response.code, 200)


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

  def test_update_config_storing_value_fails(self):
    """If storing the new value fails, an error should be raised."""
    self.openbts_connection.socket.recv.return_value = json.dumps({
      'code': 500,
    })
    with self.assertRaises(InvalidRequestError):
      self.openbts_connection.update_config('sample-key', 'sample-value')


class SIPAuthServeNominalSubscriberTestCase(unittest.TestCase):
  """Testing the openbts_component.SIPAuthServe class.

  Applying nominal uses of the 'subscribers' command and 'sipauthserve' target.
  """
  def setUp(self):
    self.sipauthserve_connection = SIPAuthServe()
    # mock a zmq socket with a simple recv return value
    self.sipauthserve_connection.socket = mock.Mock()
    self.sipauthserve_connection.socket.recv.return_value = json.dumps({
      'code': 204,
      'data': 'sample',
      'dirty': 0
    })

  def test_create_subscriber_with_ki_sends_message_and_receives_response(self):
    """Creating a subscriber with a specficied ki should send a message over
    zmq and get a response.
    """
    response = self.sipauthserve_connection.create_subscriber('sample-name',
        310150123456789, 123456789, 'abc')
    self.assertTrue(self.sipauthserve_connection.socket.send.called)
    expected_message = json.dumps({
      'command': 'subscribers',
      'action': 'create',
      'fields': {
        'name': 'sample-name',
        'imsi': '310150123456789',
        'msisdn': '123456789',
        'ki': 'abc'
      }
    })
    self.assertEqual(self.sipauthserve_connection.socket.send.call_args[0],
                     (expected_message,))
    self.assertTrue(self.sipauthserve_connection.socket.recv.called)
    self.assertEqual(response.code, 204)

  def test_create_subscriber_sans_ki_sends_message_and_receives_response(self):
    """Creating a subscriber without a specficied ki should still send a
    message over zmq and get a response.
    """
    response = self.sipauthserve_connection.create_subscriber('sample-name',
        310150123456789, 123456789)
    self.assertTrue(self.sipauthserve_connection.socket.send.called)
    expected_message = json.dumps({
      'command': 'subscribers',
      'action': 'create',
      'fields': {
        'name': 'sample-name',
        'imsi': '310150123456789',
        'msisdn': '123456789',
        'ki': ''
      }
    })
    self.assertEqual(self.sipauthserve_connection.socket.send.call_args[0],
                     (expected_message,))
    self.assertTrue(self.sipauthserve_connection.socket.recv.called)
    self.assertEqual(response.code, 204)

  def test_delete_subscriber_by_imsi(self):
    """Deleting a subscriber by passing an IMSI should send a message over zmq
    and get a response.
    """
    response = self.sipauthserve_connection.delete_subscriber(
        imsi=310150123456789)
    self.assertTrue(self.sipauthserve_connection.socket.send.called)
    expected_message = json.dumps({
      'command': 'subscribers',
      'action': 'delete',
      'match': {
        'imsi': str(310150123456789)
      }
    })
    self.assertEqual(self.sipauthserve_connection.socket.send.call_args[0],
                     (expected_message,))
    self.assertTrue(self.sipauthserve_connection.socket.recv.called)
    self.assertEqual(response.code, 204)

  def test_delete_subscriber_by_msisdn(self):
    """Deleting a subscriber by passing an MSISDN should send a message over
    zmq and get a response.
    """
    response = self.sipauthserve_connection.delete_subscriber(
        msisdn=123456789)
    self.assertTrue(self.sipauthserve_connection.socket.send.called)
    expected_message = json.dumps({
      'command': 'subscribers',
      'action': 'delete',
      'match': {
        'msisdn': str(123456789)
      }
    })
    self.assertEqual(self.sipauthserve_connection.socket.send.call_args[0],
                     (expected_message,))
    self.assertTrue(self.sipauthserve_connection.socket.recv.called)
    self.assertEqual(response.code, 204)


class SIPAuthServeOffNominalSubscriberTestCase(unittest.TestCase):
  """Testing the openbts_component.SIPAuthServe class.

  Applying off nominal uses of the 'subscribers' command and the 'sipauthserve'
  target.
  """
  def setUp(self):
    self.sipauthserve_connection = SIPAuthServe()
    # mock a zmq socket with a simple recv return value
    self.sipauthserve_connection.socket = mock.Mock()
    self.sipauthserve_connection.socket.recv.return_value = json.dumps({
      'code': 204,
      'data': 'sample',
      'dirty': 0
    })

  def test_delete_subscriber_with_both_msisdn_and_imsi(self):
    """Trying to delete a subscriber by passing an MSISDN and an IMSI should
    raise a SyntaxError -- only one param should be used.
    """
    with self.assertRaises(SyntaxError):
      self.sipauthserve_connection.delete_subscriber(msisdn=123456789,
          imsi=310150123456789)

  def test_delete_subscriber_with_neither_msisdn_and_imsi(self):
    """Trying to delete a subscriber without passing an MSISDN or an IMSI
    should raise a SyntaxError.
    """
    with self.assertRaises(SyntaxError):
      self.sipauthserve_connection.delete_subscriber()
