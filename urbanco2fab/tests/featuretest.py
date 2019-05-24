import unittest
import sys
sys.path.append("../")

from feature import Feature

class FeatureTestSuite(unittest.TestCase):
  def test_constant(self):
    feature = Feature("feature", "2019-05-22 14:09:23.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           "numberofstoreys")

if __name__ == '__main__':
  unittest.main()
