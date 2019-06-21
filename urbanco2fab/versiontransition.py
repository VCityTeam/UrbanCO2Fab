import json
from abstractfeature import AbstractFeature
from enum import Enum
from validate import Validate
from dateutil.parser import parse
from version import VersionType, Version

class VersionTransitionType(Enum):
  REGULAR = 1
  INFLUENCED = 2

class VersionTransition(AbstractFeature):
  def __init__(self, identifier, existencestarttime=None, existenceendtime=None,
          storetransactionstarttime=None, storetransactionendtime=None,
          title=None,
          fromVersion=None, toVersion=None, versiontransitiontype=None):
    super(VersionTransition, self).__init__(identifier, existencestarttime, 
            existenceendtime, storetransactionstarttime, storetransactionendtime,
            identifier+".transition")
    self.__class__ = VersionTransition
    self.title = title
    self.versiontransitiontype = versiontransitiontype
    self.fromVersion = fromVersion
    self.toVersion = toVersion
    self.validate()

  def get(self, filters=[], info=dict()):
    super(VersionTransition, self).get(filters, info)
    for fter in filters:
      if (fter == "all"):
        info["toVersion"] = self.toVersion
        info["fromVersion"] = self.fromVersion
        break
      if (fter == "fromVersion"):
        info["fromVersion"] = self.fromVersion
      if (fter == "toVersion"):
        info["toVersion"] = self.toVersion
    return info

  def validate(self):
    Validate.validateclass(VersionTransitionType, self.versiontransitiontype)
    Validate.validateclass(Version, self.fromVersion)
    Validate.validateclass(Version, self.toVersion)
    toVersionexistencestarttime = parse(self.toVersion.get(filters=
       ["existencestarttime"])["existencestarttime"])
    fromVersionexistenceendtime = parse(self.fromVersion.get(filters=
       ["existenceendtime"])["existenceendtime"])
    if(toVersionexistencestarttime < fromVersionexistenceendtime):
        raise VersionTransitionError("End time of old version must be less than the start time of the new version")
    if(toVersionexistencestarttime != parse(self.existenceendtime) and
       fromVersionexistenceendtime != parse(self.existencestarttime)):
        raise VersionTransitionError("Version transition time not continuous with from and to versions")
    
    # Influence transitions
    if(self.versiontransitiontype == VersionTransitionType.INFLUENCED):
      # Note: existence time has already been checked
      if ((self.fromVersion.get(filters=["type"])["type"] != VersionType.IMAGINARY
       and self.toVersion.get(filters=["type"])["type"] != VersionType.EXISTING) or
        (self.fromVersion.get(filters=["type"])["type"] != VersionType.IMAGINARY
       and self.toVersion.get(filters=["type"])["type"] != VersionType.EXISTING)):
        raise VersionTransitionError("Influence transition must be from imaginary to existing or imaginary to imaginary")
  

class VersionTransitionList(list):
  def __init__(self, *args):
    super(VersionTransitionList, self).__init__()
    self.__class__ = VersionTransitionList
    for arg in args:
      self.append(arg)

  def append(self, versiontransition):
    if not isinstance(versiontransition,VersionTransition):
      raise Exception("It's not a version transition: " + str(versiontransition))  
    super(VersionTransitionList, self).append(versiontransition) 

def get_versiontransition(versiontransitionids, display=True):
  all_verstiontransitions = []
  with open(".urbanco2fab/scenarios.json") as jsonfile:
    scenarios = json.load(jsonfile)
    for scenarioid in scenarios:
      for versiontransitionid in versiontransitionids:
        for versiontransition in scenarios[scenarioid]["versiontransitions"]:
          if (versiontransitionid == versiontransition):
            versiontransitiondata = scenarios[scenarioid]["versiontransitions"][versiontransition]
            all_verstiontransitions.append(versiontransitiondata)
            print("versiontransition: " + versiontransition)
            print("  type: " + versiontransitiondata["type"])
            print("  start: " + versiontransitiondata["existencestarttime"])
            print("  end: " + versiontransitiondata["existenceendtime"])
            print("  title: " + versiontransitiondata["title"])
  return all_verstiontransitions

def tag(repository, scenarioid, versiontransitionid, tags):
  try:
    with open("./.urbanco2fab/scenarios.json", "r") as jsonfile:
      scenarios = json.load(jsonfile)
      if (scenarioid in scenarios):
        if (versiontransitionid in scenarios[scenarioid]["versiontransitions"]):
          tagset = {}
          if("tag" not in scenarios[scenarioid]["versiontransitions"]):
            scenarios[scenarioid]["versiontransitions"]["tag"] = {}
          tagset = set(scenarios[scenarioid]["versiontransitions"]["tag"]).union(set(tags))
          scenarios[scenarioid]["versiontransitions"]["tag"] = list(tagset)
      print(scenarios)
    with open("./.urbanco2fab/scenarios.json", "w") as jsonfile:
      json.dump(scenarios, jsonfile,  indent=4, sort_keys=True) 
      workspace.basic_commit(repository, "saving urbanco2fab metadata");
  except Exception as e:
     print("Error in tagging: " + e);
