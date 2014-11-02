"""openbts.exceptions
core exceptions raised by the client
"""

class OpenBTSError(Exception):
  """Generic package error."""
  pass

class InvalidRequestError(OpenBTSError):
  """Raised upon invalid requests to Node Manager."""
  pass

class InvalidResponseError(OpenBTSError):
  """Invalid zmq response."""
  pass

class TimeoutError(OpenBTSError):
  """Zmq socket timeout."""
  pass
