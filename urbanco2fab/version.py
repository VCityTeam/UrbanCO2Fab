import json
import diff
import datetime
from dateutil.parser import parse
from abstractfeature import AbstractFeature
from enum import Enum
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
            identifier+".transactions")
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
      raise Exception("It's not a version: " + str(version))  
    super(VersionList, self).append(version) 

def verify_influence(influences):
  with open("./.urbanco2fab/versions.json") as jsonfile:
    versions = json.load(jsonfile)
    for influence in influences:
      data = influence.split(":")
      if(len(data)!=2):
        raise ValueError('Influence is between two versions')
      if(data[0] not in versions):
        raise ValueError('Unrecognized version: '+ data [0])
      if(data[1] not in versions):
        raise ValueError('Unrecognized version: '+ data [1])
      diff.verify_dates(versions[data[0]]["existenceendtime"],
           versions[data[1]]["existencestarttime"])
      if ((versions[data[0]]["type"] == "existing"
          and versions[data[1]]["type"] == "imagined") or
         (versions[data[0]]["type"] == "imagined"
          and versions[data[1]]["type"] == "existing")):
        raise ValueError('Influence can only between two imagined versions'+
           ' or from imagined to exisitng version')
   #no exception received

def get_all(display=True):
  all_versions = []
  with open("./.urbanco2fab/versions.json") as jsonfile:
    versions = json.load(jsonfile)
    for versionid in versions:
      versiondata = versions[versionid]
      if display:
        print("version: " + versionid)
        if("type" in versiondata):
          print("  type: " + versiondata["type"])
        print("  start: " + versiondata["existencestarttime"])
        print("  end: " + versiondata["existenceendtime"])
        print("  title: " + versiondata["title"])
  return all_versions 

def get_version(versionids, display=True):
  all_versions = []
  with open("./.urbanco2fab/versions.json") as jsonfile:
    versions = json.load(jsonfile)
    for versionid in versionids:
      if (versionid in versions):
        versiondata = versions[versionid]
        all_versions.append(versiondata)
        if display:
          print("version: " + versionid)
          if("type" in versiondata):
            print("  type: " + versiondata["type"])
          print("  start: " + versiondata["existencestarttime"])
          print("  end: " + versiondata["existenceendtime"])
          print("  title: " + versiondata["title"])
  return all_versions 

def get_version_wrt_time(past, time):
  with open("./.urbanco2fab/versions.json") as jsonfile:
    versions = json.load(jsonfile)
    for versionid in versions:
      versiondata = versions[versionid]
      versiontime = parse(versiondata["existenceendtime"])
      if ((versiontime < time and past == True) or
            (versiontime > time and past == False)):
        print("version: " + versionid)
        if("type" in versiondata):
          print("  type: " + versiondata["type"])
        print("  start: " + versiondata["existencestarttime"])
        print("  end: " + versiondata["existenceendtime"])
        print("  label: " + versiondata["title"])

def write_version(identifier, startime, endtime, storetransactionstarttime, 
        storetransactionendtime, 
        title, description=None, tag=None, document=None, versiontype="existing", userid=None, source=None):
  version = dict()
  if(parse(startime) > parse(endtime)):
    print("Start of physical existence time greater than end time")
    exit(1)
  version["identifier"] = str(identifier)
  version["existencestarttime"] = startime
  version["existenceendtime"] = endtime
  version["storetransactionstarttime"] = storetransactionstarttime
  version["storetransactionendtime"] = storetransactionendtime
  version["title"] = title
  version["description"] = description
  version["tag"] = tag
  version["source"] = source
  version["type"] = versiontype
  version["document"] = document
  version["userid"] = userid.name
  with open(".urbanco2fab/versions.json", "r") as jsonfile:
    versions = json.load(jsonfile)
    versions[str(identifier)] = version
    jsonfile.close()
  with open(".urbanco2fab/versions.json", "w") as jsonfile:
    json.dump(versions, jsonfile,  indent=4, sort_keys=True) 
    jsonfile.close()

def tag(repository, versionid, tags):
  try:
    with open("./.urbanco2fab/versions.json", "r") as jsonfile:
      versions = json.load(jsonfile)
      if (versionid in versions):
        tagset = {}
        if ("tag" not in versions[versionid]):
          versions[versionid]["tag"] = tagset
        tagset = set(versions[versionid]["tag"]).union(tags)
        versions[versionid]["tag"] = list(tagset)
    with open("./.urbanco2fab/versions.json", "w") as jsonfile:
      json.dump(versions, jsonfile,  indent=4, sort_keys=True) 
      workspace.basic_commit(repository, "saving urbanco2fab metadata");
  except Exception as e:
     print("Error in tagging: " + e);
