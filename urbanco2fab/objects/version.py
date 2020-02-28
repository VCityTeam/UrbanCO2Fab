from objects.abstractfeature import AbstractFeature
from enum import Enum
from exception.error import DataTypeError
from validate import Validate

class VersionType(Enum):
  EXISTING = 1
  IMAGINARY = 2

class Version(AbstractFeature):
  def __init__(self, identifier, existencestarttime, existenceendtime,
          storetransactionstarttime, storetransactionendtime,
          description=None, documents=None, sources=None, 
          tags=None, title=None, dtype = None, userid=None):
    super(Version, self).__init__(identifier, existencestarttime, 
            existenceendtime, storetransactionstarttime, storetransactionendtime,
            identifier+".version")
    self.__class__ = Version
    self.description = description
    self.documents = documents
    self.sources = sources
    self.tags = tags
    self.title = title
    self.type = dtype
    self.userid = userid
    self.validate()

  def validate(self):
    Validate.validateclass(VersionType, self.type)
 
  def update(self, description=None, document=None, existencestarttime=None,
          existenceendtime=None,source=None, storetransactionstarttime=None,
          storetransactionendtime=None, tag=None, title=None, dtype = None,
          userid=None
      ):  
    if (description is not None):
      self.description = description
    if (document is not None):
      self.document.add(document)
    if (existencestarttime is not None):
      self.existencestarttime = existencestarttime
    if (existenceendtime is not None):
      self.existenceendtime = existenceendtime
    if source is not None:
      self.source.add(source)
    if (storetransactionstarttime is not None):
      self.storetransactionstarttime = storetransactionstarttime
    if (storetransactionendtime is not None):
      self.storetransactionendtime = storetransactionendtime
    if tag is not None:
      self.tag.add(tag)
    if (title is not None):
      self.title = title
    if (dtype is not None):
      self.type = dtype
    if (userid is not None):
      self.userid = userid

  def get(self, filters=[], version_info=dict()):  
    super(Version, self).get(filters, version_info)
    for fter in filters:
      if (fter == "all"):
        version_info["description"] = self.description
        version_info["document"] = self.document.get(document)
        version_info["existencestarttime"] = self.existencestarttime
        version_info["existenceendtime"] = self.existenceendtime
        version_info["source"] = self.source.get(source)
        version_info["storetransactionstarttime"] = self.storetransactionendtime
        version_info["storetransactionendtime"] = self.storetransactionstarttime
        version_info["tags"] = self.tag.get(tag)
        version_info["title"] = self.title
        version_info["type"] = self.type
        version_info["userid"] = self.userid
        break # All required information has been added
      elif (fter == "description"):
        version_info["description"] = self.description
      elif (fter == "document"):
        version_info["document"] = self.document.get(document)
      elif (fter == "existencestarttime"):
        version_info["existencestarttime"] = self.existencestarttime
      elif (fter == "existenceendtime"):
        version_info["existenceendtime"] = self.existenceendtime
      elif (fter == "source"):
        version_info["source"] = self.source.get(source)
      elif (fter == "storetransactionstarttime"):
        version_info["storetransactionstarttime"] = self.storetransactionendtime
      elif (fter == "storetransactionendtime"):
        version_info["storetransactionendtime"] = self.storetransactionstarttime
      elif (fter == "tags"):
        version_info["tags"] = self.tag.get(tag)
      elif (fter == "title"):
        version_info["title"] = self.title
      elif (fter == "type"):
        version_info["type"] = self.type
      elif (fter == "userid"):
        version_info["userid"] = self.userid
    return version_info

  def __str__(self):
    return str(self.identifier)

class VersionList(list):
  def __init__(self, *args):
    super(VersionList, self).__init__()
    for arg in args:
      self.append(arg)

  def append(self, version):
    if not isinstance(version,Version):
      raise DataTypeError("It's not a version: " + str(version))  
    super(VersionList, self).append(version) 
