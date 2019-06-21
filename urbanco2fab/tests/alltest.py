import unittest

from featuretest import *
from validatetest import *
from scenariotest import *
from transactiontest import *
from workspacetest import *
from versiontest import *
from versiontransitiontest import *
 
if __name__ == '__main__':
  suite1 = FeatureTestSuite()
  suite2 = ValidationTestSuite()
  suite3 = ScenarioTestSuite()
  suite4 = VersionTransitionTestSuite()
  suite5 = WorkspaceTestSuite()
  suite6 = VersionTestSuite()
  suite7 = TransactionTestSuite()

  alltests = unittest.TestSuite([suite1, suite2, suite3, suite4, suite5, 
               suite6, suite7])
  unittest.main()
