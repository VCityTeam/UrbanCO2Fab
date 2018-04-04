class InputError(Exception):
  """Input Error"""
  def __init__(self, message):
    self.message = message

class VersionError(Exception):
  """Input Error"""
  def __init__(self, message):
    self.message = message
