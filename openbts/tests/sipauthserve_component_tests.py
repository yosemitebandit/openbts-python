"""openbts.tests.sipauthserve_component_tests
tests for the SIPAuthServe component
"""

import json
import unittest

import mock

from openbts.components import SIPAuthServe


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
