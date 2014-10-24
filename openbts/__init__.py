"""openbts
python client to the OpenBTS NodeManager

NodeManager itself provides an API to other components: SMQueue, SIPAuthServe,
OpenBTS and NodeManager itself.
"""
from .node_manager_component import NodeManager
from .openbts_component import OpenBTS
