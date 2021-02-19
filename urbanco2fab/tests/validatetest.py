import unittest
import sys
sys.path.append("./")
sys.path.append("../")

from formats.json.validate import Validate 

class ValidationTestSuite(unittest.TestCase):
  def test_basic_validation(self):
    Validate.validatejsonfile("../schema/urbanCo2Fab/workspace.schema.json","tests/workspace.json")
    Validate.validatejsonfile("../schema/urbanCo2Fab/scenarios.schema.json","tests/scenarios.json")
    Validate.validatejsonfile("../schema/urbanCo2Fab/versions.schema.json","tests/versions.json")

if __name__ == '__main__':
  unittest.main()
