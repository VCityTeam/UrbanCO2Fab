import json

def get_versiontransition(versiontransitionids, display=True):
  all_verstiontransitions = []
  with open("scenarios.json") as jsonfile:
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
            print("  label: " + versiontransitiondata["label"])
  return all_verstiontransitions
