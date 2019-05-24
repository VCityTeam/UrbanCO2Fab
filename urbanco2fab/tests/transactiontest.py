import unittest
import sys
sys.path.append("../")

from feature import Feature, FeatureList
from transaction import Transaction

class TransactionTestSuite(unittest.TestCase):
  def test_basic_transaction(self):
    feature1 = Feature("feature", "2019-05-22 14:09:23.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           "numberofstoreys")
    feature2 = Feature("feature", "2019-05-22 14:09:23.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           "numberofstoreys")
 
    featurelist = FeatureList(feature1, feature2)

    transaction = Transaction("transaction", "2019-05-22 14:09:23.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           featurelist)

if __name__ == '__main__':
  unittest.main()
