"""openbts.node_manager_component
manages connections to the NodeManager
"""
from openbts import core

class NodeManager(core.BaseConnection):
  """Manages communication to a NodeManager instance.
  """
  def __init__(self):
    super(NodeManager, self).__init__()
