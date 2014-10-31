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
