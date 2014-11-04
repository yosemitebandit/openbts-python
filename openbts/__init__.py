"""openbts
python client to the OpenBTS NodeManager

NodeManager provides an API to other components in the OpenBTS application
suite, such as the SMQueue service, SIPAuthServe, OpenBTS and NodeManager
itself.
"""

from .components import OpenBTS, SIPAuthServe, SMQueue
