"""openbts.components
manages components in the OpenBTS application suite
"""

from openbts.core import BaseComponent

class OpenBTS(BaseComponent):
  """Manages communication to an OpenBTS instance.

  Args:
    address: tcp socket for the zmq connection
  """

  def __init__(self, address='tcp://127.0.0.1:45060'):
    super(OpenBTS, self).__init__()
    self.socket.connect(address)

  def __repr__(self):
    return 'OpenBTS component'

  def monitor(self):
    """Monitor channel loads, queue sizes and noise levels.

    See 3.4.4 of the OpenBTS 4.0 Manual for more info.

    Returns:
      Response instance
    """
    message = {
      'command': 'monitor',
      'action': '',
      'key': '',
      'value': ''
    }
    return self._send_and_receive(message)


class SIPAuthServe(BaseComponent):
  """Manages communication to the SIPAuthServe service.

  Args:
    address: tcp socket for the zmq connection
  """

  def __init__(self, address='tcp://127.0.0.1:45064'):
    super(SIPAuthServe, self).__init__()
    self.socket.connect(address)

  def __repr__(self):
    return 'SIPAuthServe component'

  def get_subscribers(self):
    """Gets all subscribers.

    Returns:
      Response instance
    """
    message = {
      'command': 'subscribers',
      'action': 'read',
      'key': '',
      'value': ''
    }
    response = self._send_and_receive(message)
    return response

  def create_subscriber(self, name, imsi, msisdn, ki=''):
    """Add a subscriber.

    If the 'ki' argument is given, OpenBTS will use full auth.  Otherwise the
    system will use cache auth.  The values of IMSI, MSISDN and ki will all
    be cast to strings before the message is sent.

    Args:
      name: name of the subscriber
      imsi: IMSI of the subscriber
      msisdn: MSISDN of the subscriber
      ki: authentication key of the subscriber

    Returns:
      Response instance
    """
    message = {
      'command': 'subscribers',
      'action': 'create',
      'fields': {
        'name': name,
        'imsi': str(imsi),
        'msisdn': str(msisdn),
        'ki': str(ki)
      }
    }
    response = self._send_and_receive(message)
    return response

  def delete_subscriber(self, imsi):
    """Delete a subscriber by IMSI.

    Args:
      imsi: the IMSI of the to-be-deleted subscriber

    Returns:
      Response instance
    """
    message = {
      'command': 'subscribers',
      'action': 'delete',
      'match': {
        'imsi': str(imsi)
      }
    }
    response = self._send_and_receive(message)
    return response


class SMQueue(BaseComponent):
  """Manages communication to the SMQueue service.

  Args:
    address: tcp socket for the zmq connection
  """

  def __init__(self, address='tcp://127.0.0.1:45063'):
    super(SMQueue, self).__init__()
    self.socket.connect(address)

  def __repr__(self):
    return 'SMQueue component'
