from objects.abstractfeature import AbstractFeature
from objects.version import VersionType, Version
from exception.error import DataTypeError, VersionTransitionError
from enum import Enum
from validate import Validate
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
      raise DataTypeError("It's not a version transition: " + str(versiontransition))  
    super(VersionTransitionList, self).append(versiontransition) 
