import unittest
import sys
sys.path.append("../")

from feature import Feature, FeatureList
from transaction import Transaction, TransactionType

class TransactionTestSuite(unittest.TestCase):
  def test_basic_transaction_replace(self):
    feature1 = Feature("feature1", "2019-05-22 14:09:23.833813840+02:00",
           "2019-05-22 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           "numberofstoreys", 1)
    feature2 = Feature("feature1", "2019-05-22 14:09:23.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           "numberofstoreys", 2)
 
    featurelist = FeatureList(feature1, feature2)

    transaction = Transaction("transaction", "2019-05-22 14:09:23.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           feature1, feature2, TransactionType.REPLACE)

  def test_basic_transaction_delete(self):
    feature1 = Feature("feature1", "2019-05-22 14:09:23.833813840+02:00",
           "2019-05-22 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           "numberofstoreys", 1)

    transaction = Transaction("transaction", "2019-05-22 14:09:23.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           feature1, None, TransactionType.DELETE)

  def test_basic_transaction_insert(self):
    feature1 = Feature("feature1", "2019-05-22 14:09:23.833813840+02:00",
           "2019-05-22 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           "numberofstoreys", 1)

    transaction = Transaction("transaction", "2019-05-22 14:09:23.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           None, feature1, TransactionType.INSERT)
if __name__ == '__main__':
  unittest.main()
