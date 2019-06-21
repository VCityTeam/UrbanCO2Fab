import unittest
import sys
sys.path.append("../")

from error import *
from feature import Feature, FeatureList
from versiontransition import VersionTransition, VersionTransitionType
from version import Version, VersionType

class TransactionTestSuite(unittest.TestCase):
  def test_basic_transaction_replace(self):
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
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           title="version transition 1",
           fromVersion=version1, toVersion=version2,
           versiontransitiontype=VersionTransitionType.REGULAR)

  def test_influence_transition(self):
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
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           title="version transition 1",
           fromVersion=version1, toVersion=version2,
           versiontransitiontype=VersionTransitionType.INFLUENCED)

  def test_influence_transition_with_imaginary_versions(self):
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
          dtype = VersionType.IMAGINARY, userid="user1")

    transition = VersionTransition("versiontransition1", 
           "2019-05-21 14:09:23.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           title="version transition 1",
           fromVersion=version1, toVersion=version2,
           versiontransitiontype=VersionTransitionType.INFLUENCED)


  def test_invalid_influence_transition(self):
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


    try: 
      transition = VersionTransition("versiontransition1", 
           "2019-05-21 14:09:23.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
           title="version transition 1",
           fromVersion=version1, toVersion=version2,
           versiontransitiontype=VersionTransitionType.INFLUENCED)
    except Exception as e:
      self.assertEqual(VersionTransitionError, type(e))
      

if __name__ == '__main__':
  unittest.main()
