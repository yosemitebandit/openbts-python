"""openbts.exceptions
core exceptions raised by the client
"""

class OpenBTSError(Exception):
  """Generic package error."""
  pass

class InvalidResponseError(OpenBTSError):
  """Invalid zmq response."""
  pass
