import error
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
      repo = Repository(path)
      empty = dict() 
      for filename in ["scenarios.json", "versions.json", "workspace.json"]:
        with open(path + "/.urbanco2fab/" + filename, "w") as jsonfile:
          json.dump(empty, jsonfile,  indent=4, sort_keys=True) 
          jsonfile.close()
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
       description, tag, document, versiontype):
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
        tag, document, versiontype, user)
    basic_commit(workspace, "saving urbanco2fab metadata");
  except Exception as e:
    print("Unable to commit to UrbanCo2Fab repository: " + str(e))

def create_workspace(repository, consensusscenario, propositions, influence=[]):
  try:
    with open("./.urbanco2fab/workspace.json", "r") as jsonfile:
      workspace = json.load(jsonfile)
      if(len(consensusscenario) != 0):
        print("Only one consensus scenario allowed")
        exit(1)
      workspace["consensus"] = consensusscenario[0]
      propositionset = {}
      if("propositions" in workspace):
        propositionset = workspace["propositions"]
        workspace["propositions"] = list(propositionset.union(set(propositions)))
      influenceset = {}
      if("influence" in workspace):
        influenceset = workspace["influence"]
        version.verify_influence(influence)
        # if here no exceptions are thrown
        workspace["influence"] = list(influenceset.union(set(influence)))
    with open("./.urbanco2fab/workspace.json", "w") as jsonfile:
      json.dump(workspace, jsonfile,  indent=4, sort_keys=True) 
      basic_commit(repository, "saving urbanco2fab metadata");
  except Exception as e:
    print("Unable to create UrbanCo2Fab workspace: " + str(e))
