import unittest
import sys
sys.path.append("./")
sys.path.append("../")

from validate import Validate 

class ValidationTestSuite(unittest.TestCase):
  def test_basic_validation(self):
    Validate.validatejsonfile("../../schema/urbanCo2Fab/workspace.schema.json","workspace.json")
    Validate.validatejsonfile("../../schema/urbanCo2Fab/scenarios.schema.json","scenarios.json")
    Validate.validatejsonfile("../../schema/urbanCo2Fab/versions.schema.json","versions.json")

if __name__ == '__main__':
  unittest.main()
