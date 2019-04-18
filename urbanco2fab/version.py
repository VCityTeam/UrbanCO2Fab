import json
import diff
import workspace
import datetime
from dateutil.parser import parse

class Version:
  def __init__(self, identifier):
    self.identifier = None
    self.description = None
    self.document = list()
    self.existenceendtime = None
    self.existencestarttime = None
    self.source = list()
    self.storetransactionendtime = None
    self.storetransactionstarttime = None
    self.tag = list() 
    self.title = None
    self.type = None
    self.userid = None
 
  def add_description(self, description):  
    self.description = description
 
  def add_document(self, document):
    self.document.add(document)

  def add_existencestarttime(self, existencestarttime):
    self.existencestarttime = existencestarttime

  def add_existenceendtime(self, existenceendtime):
    self.existenceendtime = existenceendtime

  def add_source(self, source):
    self.source.add(source)

  def add_storetransactionstarttime(self, storetransactionstarttime):
    self.storetransactionendtime = None

  def add_storetransactionendtime(self, storetransactionendtime):
    self.storetransactionstarttime = storetransactionendtime

  def add_tag(self, tag):
    self.tag.add(tag)

  def add_title(self, title):
    self.title = title

  def add_type(self, dtype):
    self.type = dtype

  def add_userid(self, userid):
    self.userid = userid

  def get_description(self):  
    return self.description
 
  def get_document(self):
    return self.document.get(document)

  def get_existencestarttime(self):
    return self.existencestarttime

  def get_existenceendtime(self):
    return self.existenceendtime

  def get_source(self):
    return self.source.get(source)

  def get_storetransactionstarttime(self):
    return self.storetransactionendtime

  def get_storetransactionendtime(self):
    return self.storetransactionstarttime

  def get_tag(self):
    return self.tag.get(tag)

  def get_title(self):
    return self.title

  def get_type(self):
    return self.type

  def get_userid(self):
    return self.userid

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