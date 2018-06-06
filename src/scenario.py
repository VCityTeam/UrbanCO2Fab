import error
from pygit2 import Repository
import xmlparser
from datetime import datetime, timezone, timedelta
import json
import diff

def get_scenario(scenarioids, display=True):
  all_scenarios = []
  with open("scenarios.json") as jsonfile:
    scenarios = json.load(jsonfile)
    for scenarioid in scenarioids:
      if (scenarioid in scenarios):
        all_scenarios.append(scenarios[scenarioid])
        if(display):
          print("scenario: " + scenarioid)
          print("  versions: ")
        for version in scenarios[scenarioid]["versions"]:
          if(display):
            print("    " + version)
        if(display):
          print("  version transitions: ")
        for versiontransition in scenarios[scenarioid]["versiontransitions"]:
          if(display):
            print("    "+versiontransition)
  return all_scenarios

def create_scenario(repository, userversions, userversiontransitions, title, description):
  scenario = dict() 
  jsonfile = None
  versionsmetadata = dict()
  try:
    with open("scenarios.json", "r") as jsonfile:
      scenario = json.load(jsonfile)
      scenario[title]["title"] = title
      scenario[title]["description"] = description
  except:
    scenario[title] = dict({"title": title, "description": description})
    scenario[title]["versions"] = dict()
    scenario[title]["versiontransitions"] = dict()

  with open(".urbanco2fab/versions.json", "r") as jsonfile:
    versionsmetadata = json.load(jsonfile)

  repo = Repository(repository)
  versions, labels = [], []
  for info in userversions:
    data = info.split(":")
    if(len(data) == 1 or len(data) == 2 or len(data) == 3):
      commit = repo.get(data[0]) 
      startdate = ""
      enddate = ""
      if (commit is not None):
        tree = commit.tree
        for entry in tree:
          if(".xml" in entry.name):
            blob = repo[entry.id]
            versionstartdate, versionenddate = xmlparser.parse(blob.read_raw().decode('utf-8'))
            if(startdate == "" or startdate < versionstartdate):
              startdate = versionstartdate
            if(enddate == "" or enddate > versionenddate):
              enddate = versionenddate
      versions.append(data[0])
      label = commit.message
      versiontype = "existing"
      if (len(data) == 2):
        versiontype = data[1].lower()
      elif (len(data) == 3):
        label = data[2]
      if (versiontype != "existing" and versiontype != "regular"):
         raise error.InputError("Unrecognized version type value: " + versiontype +
                ", allowed values: existing or imagined") 
      labels.append(label)
      tzinfo  = timezone( timedelta(minutes=commit.author.offset) )
      commit_time = datetime.fromtimestamp(commit.author.time,tzinfo).strftime("%Y-%m-%dT%H:%M:%S%z")
      scenario[title]["versions"][data[0]] = dict({"label": label, "existencestarttime": str(startdate), "type": versiontype, "agentidentifier" : commit.author.name,
                       "existenceendtime" : str(enddate), "transactionstarttime" : commit_time, "transactionendtime": commit_time})
    else:
      raise error.InputError("Unrecognized version value (version:[type:label])")

  versiontransitions, labels = [], []
  startdate = ""
  enddate = ""
  for info in userversiontransitions:
    data = info.split(":")
    transitiontype = "regular"
    if(len(data) == 2):
      label = ""
    elif(len(data) == 3):
      transitiontype = data[2].lower()
    elif(len(data) == 4):
      label = data[3]
    else:
      raise error.InputError("Unrecognized version transition value (version1:version2:[label])")

    if (transitiontype != "regular" and transitiontype != "influence"):
      raise error.InputError("Unrecognized transition type value: " + transitiontype +
           ", allowed values: regular or influence") 

    if(data[0] in versions and data[1] in versions):
      versiontransitions.append([data[0],data[1]])
      transactions = None
      transactions = diff.get_transactions(repository, data[0], data[1],
             versionsmetadata[data[0]]["existenceendtime"],
             versionsmetadata[data[1]]["existencestarttime"])
      scenario[title]["versiontransitions"][data[0] + "-" + data[1]] = dict(
           {"from" : data[0], "to": data[1], "type": transitiontype,
            "existencestarttime": scenario[title]["versions"][data[0]]["existenceendtime"],
            "existenceendtime": scenario[title]["versions"][data[1]]["existencestarttime"],
            "label" : label,
            "transactions" : transactions 
           }
         )
    else:
      raise error.VersionError("Version present in verion transitions is not recognized")
    labels.append(label)

  with open("scenarios.json", "w") as jsonfile:
    json.dump(scenario, jsonfile,  indent=4, sort_keys=True) 
