import json
import workspace
import datetime
from dateutil.parser import parse

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
        title, description=None, tag=None, document=None, versiontype="existing", userid=None):
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
