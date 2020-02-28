from error import * 
import sys
from pygit2 import Repository
import parser.citygml.xmlparser
from datetime import datetime, timezone, timedelta
import json
import diff
from abstractfeature import AbstractFeature
import version
from versiontransition import *
from validate import Validate
from enum import Enum


def get_versions(scenarioid):
    with open("./.urbanco2fab/scenarios.json", "r") as jsonfile:
      scenarios = json.load(jsonfile)
      if(scenarioid not in scenarios):
        raise ValueError('Unrecognized scenario: ' + scenarioid)
      return set(scenarios[scenarioid]["versions"])
  
def verify_scenario(scenarioid):
    with open("./.urbanco2fab/scenarios.json", "r") as jsonfile:
      scenarios = json.load(jsonfile)
      if(scenarioid not in scenarios):
        raise ValueError('Unrecognized scenario: ' + scenarioid)
  
def verify_scenarios(scenarioids):
    with open("./.urbanco2fab/scenarios.json", "r") as jsonfile:
      scenarios = json.load(jsonfile)
      for scenarioid in scenarioids:
        if(scenarioid not in scenarios):
          raise ValueError('Unrecognized scenario: ' + scenarioid)
  
def get_scenario(scenarioid, display=True):
    all_scenarios = []
    with open("./.urbanco2fab/scenarios.json") as jsonfile:
      scenarios = json.load(jsonfile)
      print(scenarioid)
      if (scenarioid in scenarios):
        all_scenarios.append(scenarios[scenarioid])
        if(display):
          print("scenario: " + scenarioid)
          print("type: " + scenarios[scenarioid]["type"])
          print("  versions: ")
          for version in scenarios[scenarioid]["versions"]:
              print("    " + version)
          print("  version transitions: ")
          for versiontransition in scenarios[scenarioid]["versiontransitions"]:
            print("    "+versiontransition)
    return all_scenarios
  
def create_scenario_using_gml_dates(repository, userversions, 
      userversiontransitions, title, description, differencegraph=[]):
    scenario = dict() 
    jsonfile = None
    versionsmetadata = dict()
    try:
      with open("./.urbanco2fab/scenarios.json", "r") as jsonfile:
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
        scenario[title]["versions"][data[0]] = dict({"title": label, "existencestarttime": str(startdate), "type": versiontype, "agentidentifier" : commit.author.name,
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
               versionsmetadata[data[1]]["existencestarttime"], differencegraph)
        scenario[title]["versiontransitions"][data[0] + "-" + data[1]] = dict(
             {"from" : data[0], "to": data[1], "type": transitiontype,
              "existencestarttime": scenario[title]["versions"][data[0]]["existenceendtime"],
              "existenceendtime": scenario[title]["versions"][data[1]]["existencestarttime"],
              "title" : label,
              "transactions" : transactions 
             }
           )
      else:
        raise error.VersionError("Version present in verion transitions is not recognized")
      labels.append(label)
  
    with open("./.urbanco2fab/scenarios.json", "w") as jsonfile:
      json.dump(scenario, jsonfile,  indent=4, sort_keys=True) 
  
def create_scenario(repository, userversions, userversiontransitions, 
      title, description, scenariontype="proposition", differencegraph=[]):
    scenario = dict() 
    jsonfile = None
    versionsmetadata = dict()
    try:
      with open("./.urbanco2fab/scenarios.json", "r") as jsonfile:
        scenario = json.load(jsonfile)
        if(title in scenarios):
          raise ValueError('Existing scenario: ' + title+ ", change title")
        if(scenariontype == "consensus"):
          #verify that there is only one consensus scenario
          for scenarioid in scenario:
            if("type" in scenario[scenarioid]):
              if(scenario[scenarioid]["type"] == "consensus" and
                scenarioid != title):
                print("Consensus scenario already exists." +
                  "Only one consensus scenario can be created")
        scenario[title]["title"] = title
        scenario[title]["type"] = scenariontype 
        scenario[title]["description"] = description
    except:
      scenario[title] = dict({"title": title, "description": description})
      scenario[title]["versions"] = dict()
      scenario[title]["versiontransitions"] = dict()
  
    with open(".urbanco2fab/versions.json", "r") as jsonfile:
      versionsmetadata = json.load(jsonfile)
  
    scenario[title]["versions"] = userversions
  
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
  
      if(data[0] in userversions and data[1] in userversions):
        versiontransitions.append([data[0],data[1]])
        transactions = None
        print("in get_transactions")
        print(str(differencegraph))
        transactions = diff.get_transactions(repository, data[0], data[1],
               versionsmetadata[data[0]]["existenceendtime"],
               versionsmetadata[data[1]]["existencestarttime"], differencegraph=differencegraph)
        scenario[title]["versiontransitions"][data[0] + "-" + data[1]] = dict(
             {"from" : data[0], "to": data[1], "type": transitiontype,
              "existencestarttime": versionsmetadata[data[0]]["existenceendtime"],
              "existenceendtime": versionsmetadata[data[1]]["existencestarttime"],
              "title" : label,
              "transactions" : transactions 
             }
           )
      else:
        raise error.VersionError("Version present in verion transitions is not recognized")
      labels.append(label)
  
    with open("./.urbanco2fab/scenarios.json", "w") as jsonfile:
      json.dump(scenario, jsonfile,  indent=4, sort_keys=True) 
    Workspace.basic_commit(repository, "saving urbanco2fab metadata");
  
def tag(repository, scenarioid, tags):
    try:
      with open("./.urbanco2fab/scenarios.json", "r") as jsonfile:
        scenarios = json.load(jsonfile)
        if (scenarioid in scenarios):
          tagset = {}
          if ("tag" not in scenarios[scenarioid]):
            scenarios[scenarioid]["tag"] = {}
          tagset = set(scenarios[scenarioid]["tag"]).union(tags)
          scenarios[scenarioid]["tag"] = list(tagset)
      with open("./.urbanco2fab/scenarios.json", "w") as jsonfile:
        json.dump(scenarios, jsonfile,  indent=4, sort_keys=True) 
        Workspace.basic_commit(repository, "saving urbanco2fab metadata");
    except Exception as e:
       print("Error in tagging: " + e);
