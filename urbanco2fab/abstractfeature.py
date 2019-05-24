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
