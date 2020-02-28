import unittest

from exception.error import *
from objects.feature import Feature, FeatureList
from objects.version import *
from objects.versiontransition import * 
from objects.scenario import *
from objects.workspace import Workspace

class WorkspaceTestSuite(unittest.TestCase):
  def test_basic_workpace(self):
    vdocuments1 = ["photograph1", "photograph2"]
    vsources1 = ["source1", "source2"]
    vtags1 = ["building1", "administrative"]
    version1 = Version("version1", "2019-05-20 14:09:23.833813840+02:00",
           "2019-05-21 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
          description="Building constructed", 
          documents=vdocuments1, sources=vsources1, 
          tags=vtags1, title="version1", 
          dtype = VersionType.EXISTING, userid="user1")
    scenario = Scenario("scenario1", "2019-05-20 14:09:23.833813840+02:00",
           "2019-05-21 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
          description="Scenario of Building construction", 
          tags=vtags1, title="scenario1", 
          versions = [version1], versiontransitions=None,
          scenariotype = ScenarioType.CONSENSUS, userid="user1")

    workspace = Workspace("workspace1", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
          description="Workspace", 
          tags=vtags1, title="workspace1", 
          consensusscenario = scenario, userid="user1")

  def test_basic_workpace_with_common_scenario(self):
    vdocuments1 = ["photograph1", "photograph2"]
    vsources1 = ["source1", "source2"]
    vtags1 = ["building1", "administrative"]
    version1 = Version("version1", "2019-05-20 14:09:23.833813840+02:00",
           "2019-05-21 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
          description="Building constructed", 
          documents=vdocuments1, sources=vsources1, 
          tags=vtags1, title="version1", 
          dtype = VersionType.EXISTING, userid="user1")
 
    vdocuments2 = ["photograph1", "photograph2"]
    vsources2 = ["source1", "source2"]
    vtags2 = ["building1", "administrative"]
    version2 = Version("version1", "2019-05-22 14:09:23.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
          description="Building constructed",
          documents=vdocuments2, sources=vsources2, 
          tags=vtags2, title="version2", 
          dtype = VersionType.EXISTING, userid="user1")

    transition = VersionTransition("versiontransition1", 
           "2019-05-21 14:09:23.833813840+02:00",
           "2019-05-22 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           title="version transition 1",
           fromVersion=version1, toVersion=version2,
           versiontransitiontype=VersionTransitionType.REGULAR)

    versiontransitionlist = VersionTransitionList(transition)
    versionlist = VersionList(version1, version2)

    scenario = Scenario("scenario1", "2019-05-20 14:09:20.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
          description="Scenario of Building construction", 
          tags=vtags1, title="scenario1", 
          versions = versionlist, versiontransitions=versiontransitionlist,
          scenariotype = ScenarioType.CONSENSUS, userid="user1")

    try:
      workspace = Workspace("workspace1", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
          description="Workspace", 
          tags=vtags1, title="workspace1", 
          consensusscenario = scenario, 
          propositionscenarios = ScenarioList(scenario), 
          userid="user1")
    except Exception as e:
      self.assertEqual(ConsensusScenarioError, type(e))

  def test_basic_workpace_with_propositions(self):
    vdocuments1 = ["photograph1", "photograph2"]
    vsources1 = ["source1", "source2"]
    vtags1 = ["building1", "administrative"]
    version1 = Version("version1", "2019-05-20 14:09:23.833813840+02:00",
           "2019-05-21 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
          description="Building constructed", 
          documents=vdocuments1, sources=vsources1, 
          tags=vtags1, title="version1", 
          dtype = VersionType.EXISTING, userid="user1")
 
    vdocuments2 = ["photograph1", "photograph2"]
    vsources2 = ["source1", "source2"]
    vtags2 = ["building1", "administrative"]
    version2 = Version("version2", "2019-05-22 14:09:23.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
          description="Building constructed",
          documents=vdocuments2, sources=vsources2, 
          tags=vtags2, title="version2", 
          dtype = VersionType.EXISTING, userid="user1")

    transition = VersionTransition("versiontransition1", 
           "2019-05-21 14:09:23.833813840+02:00",
           "2019-05-22 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           title="version transition 1",
           fromVersion=version1, toVersion=version2,
           versiontransitiontype=VersionTransitionType.REGULAR)

    versiontransitionlist = VersionTransitionList(transition)
    versionlist = VersionList(version1, version2)

    scenario = Scenario("scenario1", "2019-05-20 14:09:20.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
          description="Scenario of Building construction", 
          tags=vtags1, title="scenario1", 
          versions = versionlist, versiontransitions=versiontransitionlist,
          scenariotype = ScenarioType.CONSENSUS, userid="user1")

    pscenario = Scenario("scenario2", "2019-05-20 14:09:20.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
          description="Scenario of Building construction", 
          tags=vtags1, title="scenario1", 
          versions = versionlist, versiontransitions=versiontransitionlist,
          scenariotype = ScenarioType.CONSENSUS, userid="user1")

    workspace = Workspace("workspace1", "2019-05-20 14:09:23.833813840+02:00",
           "2019-05-24 14:09:23.833813845+02:00",
          description="Workspace", 
          tags=vtags1, title="workspace1", 
          consensusscenario = scenario, 
          propositionscenarios = ScenarioList(pscenario), 
          userid="user1")

  def test_workpace_with_imaginary_versions_consensus(self):
    vdocuments1 = ["photograph1", "photograph2"]
    vsources1 = ["source1", "source2"]
    vtags1 = ["building1", "administrative"]
    version1 = Version("version1", "2019-05-20 14:09:23.833813840+02:00",
           "2019-05-21 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
          description="Building constructed", 
          documents=vdocuments1, sources=vsources1, 
          tags=vtags1, title="version1", 
          dtype = VersionType.IMAGINARY, userid="user1")
    scenario = Scenario("scenario1", "2019-05-20 14:09:23.833813840+02:00",
           "2019-05-21 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
          description="Scenario of Building construction", 
          tags=vtags1, title="scenario1", 
          versions = [version1], versiontransitions=None,
          scenariotype = ScenarioType.CONSENSUS, userid="user1")
    
    try:
      workspace = Workspace("workspace1", "2019-05-20 14:09:23.833813840+02:00",
           "2019-05-24 14:09:23.833813845+02:00",
          description="Workspace", 
          tags=vtags1, title="workspace1", 
          consensusscenario = scenario, userid="user1")
    except Exception as e:
      self.assertEqual(ConsensusScenarioError, type(e))


if __name__ == '__main__':
  unittest.main()
