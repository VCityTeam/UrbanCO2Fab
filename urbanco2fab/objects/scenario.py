from enum import Enum
from formats.json.validate import Validate
from exception.error import ScenarioError,DataTypeError
from dateutil.parser import parse
from objects.abstractfeature import AbstractFeature
from objects.versiontransition import *

class ScenarioType(Enum):
  CONSENSUS = 1
  PROPOSITION = 2

class Scenario(AbstractFeature):
  def __init__(self, identifier, existencestarttime=None, existenceendtime=None,
          storetransactionstarttime=None, storetransactionendtime=None,
          title=None, description=None,scenariotype=None,tags=None,
          versions=None, versiontransitions=None, userid=None):
    super(Scenario, self).__init__(identifier, existencestarttime, 
            existenceendtime, storetransactionstarttime, storetransactionendtime,
            identifier+".scenario")
    self.__class__ = Scenario
    self.description = description
    self.tags = tags
    self.title = title
    self.versiontransitions = versiontransitions
    self.versions = versions
    self.userid = userid
    self.validate()

  def validate(self):
    if(self.versiontransitions is not None):
      Validate.validateclass(VersionTransitionList, self.versiontransitions)
    """
      Verify, there is a continuity of version transitions.
      First, we verify, whether size of version list is one more than size
      of version transition list
    """
    if(self.versiontransitions is not None):
      if(len(self.versiontransitions)+1 != len(self.versions)):
        raise(ScenarioError("Size of version list must be one more than size of version transition list"))
       # Next, we verify continuity
      vpos = 0 
      for versiontransition in self.versiontransitions: 
        if(parse(self.versions[vpos].get(filters=["existenceendtime"])["existenceendtime"]) !=  
          parse(versiontransition.get(filters=["existencestarttime"])["existencestarttime"])):
          raise(ScenarioError("There must be continuity between versions and version transitions"))
        if(parse(self.versions[vpos+1].get(filters=["existencestarttime"])["existencestarttime"]) !=  
         parse(versiontransition.get(filters=["existenceendtime"])["existenceendtime"])):
          raise(ScenarioError("There must be continuity between versions and version transitions"))
    else:
      if(1 != len(self.versions)):
        raise(ScenarioError("Size of version list must be one"))
     

  def get(self, filters=[], info=dict()):
    super(Scenario, self).get(filters, info)
    for fter in filters:
      if (fter == "all"):
        info["versiontransitions"] = self.versiontransitions
        info["versions"] = self.versions
        info["title"] = self.title
        info["description"] = self.description
        info["tags"] = self.tags
        info["userid"] = self.userid
        break
      if (fter == "description"):
        info["description"] = self.description
      if (fter == "versions"):
        info["versions"] = self.versions
      if (fter == "userid"):
        info["userid"] = self.userid
      if (fter == "tags"):
        info["tags"] = self.tags
      if (fter == "title"):
        info["title"] = self.title
      if (fter == "versiontransitions"):
        info["versiontransitions"] = self.versiontransitions
    return info

class ScenarioList(list):
  def __init__(self, *args):
    super(ScenarioList, self).__init__()
    for arg in args:
      self.append(arg)

  def append(self, scenario):
    if not isinstance(scenario,Scenario):
      raise DataTypeError("It's not a scenario: " + str(scenario))  
    super(ScenarioList, self).append(scenario) 
