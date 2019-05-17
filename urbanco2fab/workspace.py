import error
import sys
import version
import json
import scenario
from shutil import copyfile
from pygit2 import Repository, credentials
from datetime import datetime, timezone, timedelta
import os
import re
import diff
from pygit2 import clone_repository, init_repository, GIT_OBJ_COMMIT, GIT_SORT_REVERSE, GIT_SORT_TOPOLOGICAL

class Workspace:
  def __init__(self, jsonfilepath):
    """ Initializes a workspace by reading the JSON file containing the 
        details of a workspace. A workspace contains one consensus scenario
        and multiple (zero or more)  proposition scenarios. It may also contain
        influence transitions, that are (imaginary) transitions to show a version 
        may have influenced another version.

    Attributes
    -------
    identifier: str
      unique identifier of a workspace
    consensus_scenario: str
      unique consensus scenario of a workspace
    influence_transitions: array
      array of zero or more influence transitions
    proposition_scenarios: array
      array of zero or more proposition scenarios 

    Methods
    -------
    add_consensus_scenario(self, consensus_scenario)
       adds a consensus scenario to the workspace
    add_influence_transition(self, influence_transition)
       adds a influence transition to the workspace
    add_proposition_scenario(self, proposition_scenario)
       adds zero or more proposition scenarios to the workspace
    get_identifier(self)
       returns the (unique) identifier of the workspace
    get_consensus_scenario(self)
       returns the (unique) consensus scenario of the workspace
    get_influence_transitions(self)
       returns identifiers of influence transitions of the workspace
    get_proposition_scenarios(self)
       returns identifiers of proposition scenarios of the workspace
    
    """
    with open(jsonfilepath) as jsonfile:
      workspace = json.load(jsonfile)
    self.identifier = workspace["identifier"]
    self.consensus_scenario = workspace["consensus"]
    self.influence_transitions = workspace["influence"]
    self.proposition_scenarios = workspace["propositions"]

  def add_consensus_scenario(self, consensus_scenario):
    """
       adds a consensus scenario to the workspace. If there is already one,
       it will be replaced by the new consensus scenario

       Parameters
       ----------
       consensus_scenario: str
         the new consensus scenario to be added or replaced

       Returns
       -------
         None

       Raises
       ------ 
         None
    """
    self.consensus_scenario = consensus_scenario

  def add_influence_transition(self, influence_transition):
    """
       adds an influence transition  to the workspace. 

       Parameters
       ----------
       consensus_scenario: str
         the new influence transition to be added

       Returns
       -------
         None

       Raises
       ------ 
         None
    """
    self.influence_transitions.add(influence_transition)

  def add_proposition_scenario(self, proposition_scenario):
    """
       adds a proposition scenario to the workspace.

       Parameters
       ----------
       proposition_scenario: str
         the new proposition scenario to be added

       Returns
       -------
         None

       Raises
       ------ 
         None 
    """
    self.proposition_scenarios.add(proposition_scenario)

  def get_identifier(self):
    """
       returns the (unique) identifier of the workspace

       Parameters
       ----------
         None

       Returns
       -------
         str
          identifier of the workspace

       Raises
       ------ 
         None
    """
    return self.identifier

  def get_consensus_scenario(self):
    """
       returns the (unique) consensus scenario identifier of the workspace

       Parameters
       ----------
         None

       Returns
       -------
         str:
           identifier of the consensus scenario

       Raises
       ------ 
         None 
    """
    return self.consensus_scenario

  def get_influence_transitions(self):
    """
       returns the identifiers of influence transitions of the workspace

       Parameters
       ----------
         None

       Returns
       -------
         set of identifiers of influence transitions

       Raises
       ------ 
         None 
    """
    return self.influence_transitions

  def get_proposition_scenarios(self):
    """
       returns the identifiers of proposition scenarios of the workspace

       Parameters
       ----------
         None

       Returns
       -------
         set
           identifiers of proposition scenarios

       Raises
       ------ 
         None
    """
    return self.proposition_scenarios

#Reference: https://stackoverflow.com/questions/27749418/implementing-pull-with-pygit2
def pull(repository):
  try:
    repo = Repository(repository)
    for remote in repo.remotes:
      remote.fetch()
      remote_master_id = repo.lookup_reference('refs/remotes/origin/master').target
      master_ref = repo.lookup_reference('refs/heads/master')
      master_ref.set_target(remote_master_id)
      repo.head.set_target(remote_master_id)
  except Exception as e:
    print(e)
    print("Unable to pull from UrbanCo2Fab repository: " + str(e))

def push(repository):
  try:
    repo = Repository(repository)
    for remote in repo.remotes:
      sshcred = credentials.Keypair('git','','','')
      remote.credentials = sshcred
      remote.push(["refs/heads/master"])
  except Exception as e:
    print(e)
    print("Unable to push to UrbanCo2Fab repository: " + str(e))

def clone(repository, path, bare=False):
  try:
    if(path is not None):
      reponame = re.sub(".*/","", repository)
      reponame = reponame.replace(".git","")
      path = path + "/" + reponame
      if(bare):
        repo = clone_repository(repository, path, bare=True)
      else:
        repo = clone_repository(repository, path)
      if(os.access(path + "/.urbanco2fab", os.F_OK) == False):
        os.makedirs(path + "/.urbanco2fab") 
  except Exception as e:
    print("Not a valid UrbanCo2Fab repository: " + str(e))

def init(path, bare=False):
  try:
    if(path is not None):
      if(bare):
        repo = init_repository(path, bare=True)
        return
      else:
        repo = init_repository(path)

      #creating urbanco2fab directory and adding it to git metadata mgmt.
      os.makedirs(path + "/.urbanco2fab") 
      copyfile(os.path.dirname(__file__)+ "/viz.js", ".urbanco2fab/viz.js")
      copyfile(os.path.dirname(__file__)+ "/full.render.js", ".urbanco2fab/full.render.js")
       
      repo = Repository(path)
      empty = dict() 
      for filename in ["scenarios.json", "versions.json", "workspace.json"]:
        with open(path + "/.urbanco2fab/" + filename, "w") as jsonfile:
          json.dump(empty, jsonfile,  indent=4, sort_keys=True) 
          jsonfile.close()
          repo.index.add(".urbanco2fab/"+filename)
      for filename in ["viz.js", "full.render.js"]:
        repo.index.add(".urbanco2fab/"+filename)
      repo.index.write()
      basic_commit(path, "Initilizing UrbanCo2Fab")
    else:
      print("path missing")
  except Exception as e:
    print("Not a valid UrbanCo2Fab repository: " + str(e))

def add(workspace, paths=None):
  try:
    repo = Repository(workspace)
    if (paths is not None):
      for path in paths:
        repo.index.add(path)
    repo.index.write()
  except Exception as e:
    print("Unable to add to UrbanCo2Fab repository: " + str(e))

def move(workspace, paths=None):
  try:
    if (paths is not None):
      repo = Repository(workspace)
      if(len(paths) == 2):
        copyfile(paths[0], paths[1])
        os.remove(paths[0])
        repo.index.add(paths[1])
        repo.index.write()
      else:
        print("Move requires two paths") 
  except Exception as e:
    print("Unable to remove from UrbanCo2Fab repository: " + str(e))

def rm(workspace, paths=None):
  try:
    if (paths is not None):
      repo = Repository(workspace)
      for path in paths:
        repo.index.remove(path)
      repo.index.write()
  except Exception as e:
    print("Unable to remove from UrbanCo2Fab repository: " + str(e))

def tag(workspace, name, message, commitid=None):
  try:
    repo = Repository(workspace)
    if (commitid is None):
      commitid = repo.head.target
    repo.create_tag(name, commitid, GIT_OBJ_COMMIT, 
         repo.default_signature, message)
  except Exception as e:
    print("Unable to tag a UrbanCo2Fab repository: " + str(e))

def basic_commit(workspace, message):
  try:
    repo = Repository(workspace)
    for filename in ["scenarios.json", "versions.json"]:
      repo.index.add(".urbanco2fab/"+filename)
    user = repo.default_signature
    #https://stackoverflow.com/questions/29469649/create-a-commit-using-pygit2
    tree = repo.index.write_tree()
    if repo.head_is_unborn:
      parents = []
    else:
      parents = [repo.head.target]
    repo.index.write()
    repo.create_commit('HEAD', user, user, message, tree, parents)
    repo.index.write()
  except Exception as e:
    print("Unable to commit to UrbanCo2Fab repository: " + str(e))

def commit(workspace, message, starttime, endtime,
       description, tag, document, versiontype, source):
  try:
    repo = Repository(workspace)
    user = repo.default_signature
    #https://stackoverflow.com/questions/29469649/create-a-commit-using-pygit2
    tree = repo.index.write_tree()
    if repo.head_is_unborn:
      parents = []
    else:
      parents = [repo.head.target]
    repo.create_commit('HEAD', user, user, message, tree, parents)
    repo.index.write()
    tzinfo  = timezone( timedelta(minutes=repo[repo.head.target].author.offset) )
    storetransactionendtime = datetime.fromtimestamp(repo[repo.head.target].author.time,tzinfo).strftime("%Y-%m-%dT%H:%M:%S%z")
    version.write_version(repo.head.target, starttime, endtime, 
        storetransactionendtime, storetransactionendtime, message, description, 
        tag, document, versiontype, user, source)
    basic_commit(workspace, "saving urbanco2fab metadata");
  except Exception as e:
    print("Unable to commit to UrbanCo2Fab repository: " + str(e))


def create_workspace(repository, consensusscenario, propositions, influence=[]):
  try:
    with open("./.urbanco2fab/workspace.json", "r") as jsonfile:
      workspace = json.load(jsonfile)
    with open("./.urbanco2fab/scenarios.json", "r") as jsonfile:
      scenarios = json.load(jsonfile)
      if(len(consensusscenario) != 1):
        print("Only one consensus scenario allowed")
        exit(1)
      scenario.verify_scenario(consensusscenario[0])
      scenario.verify_scenarios(propositions)
      workspace["consensus"] = consensusscenario[0]
      propositionset = set(propositions)
      if("propositions" in workspace):
        propositionset = set(workspace["propositions"])
      workspace["propositions"] = list(propositionset.union(set(propositions)))

      consensusversions = scenario.get_versions(consensusscenario[0])
      common_version_present = False
      propositionversions = set()
      for propositionscenario in propositionset:
        propositionversions = propositionversions.union(scenario.get_versions(propositionscenario))
      if (len(consensusversions.intersection(propositionversions)) > 0):
          #common version found
          common_version_present = True
      if(common_version_present == False):
        raise ValueError('No common version found between consensus and proposition scenario')
      influenceset = set()
      if("influence" in workspace):
        influenceset = set(workspace["influence"])
      version.verify_influence(influence)
        # if here no exceptions are thrown
      workspace["influence"] = list(influenceset.union(set(influence)))
    with open("./.urbanco2fab/workspace.json", "w") as jsonfile:
      json.dump(workspace, jsonfile,  indent=4, sort_keys=True) 
      basic_commit(repository, "saving urbanco2fab metadata");
  except Exception as e:
    print("Unable to create UrbanCo2Fab workspace: " + str(e))

def get_workspace():
  try:
    with open("./.urbanco2fab/workspace.json", "r") as jsonfile:
      workspace = json.load(jsonfile)
      print("consensus: " + workspace["consensus"])
      print("propositions: ")
      for proposition in workspace["propositions"]:
        print("      " + proposition)
      print("influences: ")
      for influence in workspace["influence"]:
        print("      " + influence)
  except Exception as e:
    print("Unable to open UrbanCo2Fab workspace: " + str(e))

