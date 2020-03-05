import unittest

from tests.featuretest import *
from tests.validatetest import *
from tests.scenariotest import *
from tests.transactiontest import *
from tests.workspacetest import *
from tests.versiontest import *
from tests.storefactorytest import *
from tests.versiontransitiontest import *
 
if __name__ == '__main__':
  suite1 = FeatureTestSuite()
  suite2 = ValidationTestSuite()
  suite3 = ScenarioTestSuite()
  suite4 = VersionTransitionTestSuite()
  suite5 = WorkspaceTestSuite()
  suite6 = VersionTestSuite()
  suite7 = TransactionTestSuite()
  suite8 = StoreFactoryTestSuite()

  alltests = unittest.TestSuite([suite1, suite2, suite3, suite4, suite5, 
               suite6, suite7, suite8])
  unittest.main()
