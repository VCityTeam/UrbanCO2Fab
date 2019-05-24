from abc import ABC
from abc import abstractmethod
from dateutil.parser import parse

class AbstractFeature(ABC):
  @abstractmethod
  def __init__(self, identifier, existencestarttime=None, existenceendtime=None,
          storetransactionstarttime=None, storetransactionendtime=None,
          name=None, value=None):
    self.__class__ = AbstractFeature
    self.name = name
    self.value = value
    self.identifier = identifier
    self.existencestarttime = existencestarttime
    self.existenceendtime = existenceendtime
    self.storetransactionstarttime = storetransactionstarttime
    self.storetransactionendtime = storetransactionendtime
    self.validate()

  @abstractmethod
  def validate(self):
    if(self.identifier == None):
      raise Exception("Feature identifier cannot be empty")
    if(self.name == None):
      raise Exception("Feature name cannot be empty")
    if(parse(self.existencestarttime) > parse(self.existenceendtime)):
      raise Exception("Existence start time greater than the end time")
    if(parse(self.storetransactionstarttime) > parse(self.storetransactionendtime)):
      raise Exception("Store transaction start time greater than the end time")

  @abstractmethod
  def get(self, filters=[], info=dict()):
    for fter in filters:
      if (fter == "all"):
        info["existencestarttime"] = self.existencestarttime
        info["existenceendtime"] = self.existenceendtime
        info["storetransactionstarttime"] = self.storetransactionendtime
        info["storetransactionendtime"] = self.storetransactionstarttime
        info["name"] = self.name
        info["value"] = self.value
        info["identifier"] = self.identifier
        break # All required information has been added
      elif (fter == "identifier"):
        info["identifier"] = self.identifier
      elif (fter == "name"):
        info["name"] = self.name
      elif (fter == "value"):
        info["value"] = self.value
      elif (fter == "existencestarttime"):
        info["existencestarttime"] = self.existencestarttime
      elif (fter == "existenceendtime"):
        info["existenceendtime"] = self.existenceendtime
      elif (fter == "storetransactionstarttime"):
        info["storetransactionstarttime"] = self.storetransactionendtime
      elif (fter == "storetransactionendtime"):
        info["storetransactionendtime"] = self.storetransactionstarttime
    return info
