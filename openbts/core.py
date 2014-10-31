"""openbts.core
defines the base component and responses
"""

import json

import zmq

from openbts.exceptions import InvalidRequestError, InvalidResponseError

class BaseComponent(object):
  """Manages a zeromq connection.

  The intent is to create other components that inherit from this base class.

  """
  def __init__(self):
    context = zmq.Context()
    # the component inheriting from BaseComponent should call connect on this
    # socket with the appropriate address
    self.socket = context.socket(zmq.REQ)
    # TODO(matt): implement zmq timeout

  def read_config(self, key):
    """Reads a config value.

    Args:
      key: the config parameter to inspect

    Returns:
      Response instance
    """
    message = {
      'command': 'config',
      'action': 'read',
      'key': key,
      'value': ''
    }
    return self._send_and_receive(message)

  def update_config(self, key, value):
    """Updates a config value.

    Args:
      key: the config parameter to update
      value: set the config parameter to this value

    Returns:
      Response instance
    """
    message = {
      'command': 'config',
      'action': 'read',
      'key': key,
      'value': value
    }
    return self._send_and_receive(message)

  def _send_and_receive(self, message):
    """sending payloads to NM and returning Response instances.

    Or, if the action failed, instantiating a response will raise an error.

    Args:
      message: dict of a message to send to NM

    Returns:
      Response instance if the request succeeded
    """
    self.socket.send(json.dumps(message))
    raw_response_data = self.socket.recv()
    return Response(raw_response_data)


class Response(object):
  """Provides access to the response data.

  Raises an exception if the request was not successful (e.g. key not found).

  Note that we are explicitly ignoring NodeManager error code 501 (unknown
  action).  We are tightly controlling the specified action, so we do not
  expect to encounter this error.

  Args:
    raw_response_data: json-encoded text

  Attributes:
    code: the response code
    data: text or dict of response data
    dirty: boolean that, if True, indicates that the command will take effect
        on restart of the component
  """

  success_codes = [200, 204]
  error_codes = [404, 406, 409, 500]

  def __init__(self, raw_response_data):
    """Init the response with raw data from the socket."""
    data = json.loads(raw_response_data)

    if 'code' not in data.keys():
      raise InvalidResponseError('key "code" not in raw response: "%s"' %
                                 raw_response_data)

    # if request was successful, create a response object
    if data['code'] in self.success_codes:
      self.code = data['code']
      self.data = data['data']
      self.dirty = bool(data['dirty'])
    # if request failed for some reason, continue

    elif data['code'] in self.error_codes:
      if data['code'] == 404:
        raise InvalidRequestError('unknown key')
      if data['code'] == 406:
        raise InvalidRequestError('invalid value')

    # unknown response code
    else:
      raise InvalidResponseError('code "%s" not known' % data['code'])
