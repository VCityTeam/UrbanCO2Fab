import json
import datetime
from dateutil.parser import parse

def get_version(versionids, display=True):
  all_versions = []
  with open("scenarios.json") as jsonfile:
    scenarios = json.load(jsonfile)
    for scenarioid in scenarios:
      for versionid in versionids:
        for version in scenarios[scenarioid]["versions"]:
          if (versionid == version):
            versiondata = scenarios[scenarioid]["versions"][version]
            all_versions.append(versiondata)
            if display:
              print("version: " + version)
              print("  type: " + versiondata["type"])
              print("  start: " + versiondata["existencestarttime"])
              print("  end: " + versiondata["existenceendtime"])
              print("  label: " + versiondata["label"])
  return all_versions 

def get_version_wrt_time(past, time):
  with open("scenarios.json") as jsonfile:
    scenarios = json.load(jsonfile)
    for scenarioid in scenarios:
      for version in scenarios[scenarioid]["versions"]:
        versiondata = scenarios[scenarioid]["versions"][version]
        versiontime = parse(versiondata["existenceendtime"])
        if ((versiontime < time and past == True) or
            (versiontime > time and past == False)):
          print("version: " + version)
          print("  type: " + versiondata["type"])
          print("  start: " + versiondata["existencestarttime"])
          print("  end: " + versiondata["existenceendtime"])
          print("  label: " + versiondata["label"])
