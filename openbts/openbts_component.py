"""openbts.openbts_component
manages connections to OpenBTS
"""
from openbts import core

class OpenBTS(core.BaseConnection):
  """Manages communication to an OpenBTS instance.
  """
  def __init__(self):
    super(OpenBTS, self).__init__()
