"""openbts.components
manages components in the OpenBTS application suite
"""

from openbts.core import BaseComponent

class OpenBTS(BaseComponent):
  """Manages communication to an OpenBTS instance.
  """
  def __init__(self, address='tcp://127.0.0.1:45060'):
    super(OpenBTS, self).__init__()
    self.socket.connect(address)


class SIPAuthServe(BaseComponent):
  """Manages communication to the SIPAuthServe service.
  """
  def __init__(self, address='tcp://127.0.0.1:45064'):
    super(SIPAuthServe, self).__init__()
    self.socket.connect(address)

  def create_subscriber(self, name, imsi, msisdn, ki=''):
    """Add a subscriber.

    If the 'ki' argument is given, OpenBTS will use full auth.  Otherwise the
    system will use cache auth.

    Args:
      name: name of the subscriber
      imsi: IMSI of the subscriber
      msisdn: MSISDN of the subscriber
      ki: authentication key of the subscriber
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
