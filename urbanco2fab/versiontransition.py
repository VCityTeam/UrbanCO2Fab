import json
from enum import Enum
from abstractfeature import AbstractFeature
from validate import Validate
from dateutil.parser import parse

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
