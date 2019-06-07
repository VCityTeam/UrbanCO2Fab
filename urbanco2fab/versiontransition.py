import json
import workspace
from abstractfeature import AbstractFeature
from enum import Enum
from validate import Validate
from version import Version
from dateutil.parser import parse

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
    super(Transaction, self).get(filters, info)
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
        raise Exception("End time of old version must be less than the start time of the old version")
    if(toVersionexistencestarttime != parse(self.existenceendtime) and
       fromVersionexistenceendtime != parse(self.existencestarttime)):
        raise Exception("Version transition time not continuous with from and to versions")

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
