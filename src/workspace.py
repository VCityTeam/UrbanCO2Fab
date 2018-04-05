import error
import scenario
from shutil import copyfile
from pygit2 import Repository, credentials
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
  except Exception as e:
    print("Not a valid UrbanCo2Fab repository: " + str(e))

def init(path, bare=False):
  try:
    if(path is not None):
      if(bare):
        repo = init_repository(path, bare=True)
      else:
        repo = init_repository(path)
    else:
      print("path missing")
  except Exception as e:
    print("Not a valid UrbanCo2Fab repository: " + str(e))

def add(workspace, paths=None):
  try:
    repo = Repository(workspace)
    repo.index.add_all(paths)
    repo.index.write()
  except Exception as e:
    print("Unable to add to UrbanCo2Fab repository: " + str(e))

def move(workspace, paths=None):
  try:
    if (paths is not None):
      repo = Repository(workspace)
      if(len(paths) == 2):
        copyfile(paths[0], paths[1])
        repo.index.remove(paths[0])
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

def commit(workspace, message):
  try:
    repo = Repository(workspace)
    user = repo.default_signature
    tree = repo.TreeBuilder().write()
    if repo.head_is_unborn:
      parents = []
    else:
      parents = [repo.head.target]
    repo.create_commit('HEAD', user, user, message, tree, parents)
    repo.index.write()
  except Exception as e:
    print("Unable to commit to UrbanCo2Fab repository: " + str(e))

