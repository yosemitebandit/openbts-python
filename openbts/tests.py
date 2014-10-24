"""openbts.tests
tests for the primary modules
"""
import unittest

import openbts

class CoreTest(unittest.TestCase):
  """Testing the openbts.core classes.
  """
  def setUp(self):
    pass


class NodeManagerTest(unittest.TestCase):
  """Testing the openbts.NodeManager class.
  """
  def setUp(self):
    self.node_manager_connection = openbts.NodeManager()

  def test_node_manager_class_is_subclass_of_base_connection(self):
    """the package's NodeManager should be a subclass of core's BaseConnection
    """
    assert issubclass(openbts.NodeManager, openbts.core.BaseConnection)


class OpenBTSTest(unittest.TestCase):
  """Testing the openbts.OpenBTS class.
  """
  def setUp(self):
    self.openbts_connection = openbts.OpenBTS()

  def test_openbts_class_is_subclass_of_base_connection(self):
    """the package's OpenBTS should be a subclass of core's BaseConnection
    """
    assert issubclass(openbts.OpenBTS, openbts.core.BaseConnection)
