class InputError(Exception):
  """Input Error"""
  def __init__(self, message):
    self.message = " " + message

class VersionError(Exception):
  """Input Error"""
  def __init__(self, message):
    self.message = "" + message

class DataTypeError(Exception):
  """Data type Error"""
  def __init__(self, message):
    self.message = "Wrong type :"+ message

class ConsensusScenarioError(Exception):
  """Input Error"""
  def __init__(self, message):
    self.message = "Error in creating consensus scenario: " + message
