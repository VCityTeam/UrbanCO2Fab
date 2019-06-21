class InputError(Exception):
  """Input Error"""
  def __init__(self, message):
    self.message = " " + message

class VersionError(Exception):
  """Version Error"""
  def __init__(self, message):
    self.message = "Error in creating version: " + message

class VersionTransitionError(Exception):
  """Version Transition Error"""
  def __init__(self, message):
    self.message = "Error in creating version transition: " + message

class DataTypeError(Exception):
  """Data type Error"""
  def __init__(self, message):
    self.message = "Wrong type :"+ message

class ScenarioError(Exception):
  """Scenario Error"""
  def __init__(self, message):
    self.message = "Error in creating scenario: " + message

class ConsensusScenarioError(Exception):
  """Consensus scenario Error"""
  def __init__(self, message):
    self.message = "Error in creating consensus scenario: " + message
