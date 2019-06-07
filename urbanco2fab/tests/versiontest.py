import unittest
import sys
sys.path.append("../")

from version  import Version, VersionList, VersionType

class VersionTestSuite(unittest.TestCase):
  def test_basic_version(self):
    vdocuments = ["photograph1", "photograph2"]
    vsources = ["source1", "source2"]
    vtags = ["building1", "administrative"]
    version = Version("version1", "2019-05-22 14:09:23.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813840+02:00", 
           "2019-05-24 14:09:23.833813845+02:00",
          description="Building constructed", documents=vdocuments, sources=vsources, 
          tags=vtags, title="version1", 
          dtype = VersionType.EXISTING, userid="user1")

  def test_basic_versionlist(self):
    vdocuments1 = ["photograph1", "photograph2"]
    vsources1 = ["source1", "source2"]
    vtags1 = ["building1", "administrative"]
    version1 = Version("version1", "2019-05-22 14:09:23.833813840+02:00",
           "2019-05-23 14:09:23.833813840+02:00", 
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

    versionlist = VersionList(version1, version2)

if __name__ == '__main__':
  unittest.main()
