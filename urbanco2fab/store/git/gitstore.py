from store.abstractstore import AbstractStore
from objects.workspace import Workspace
from store.git.workspace import Workspace as WorkspaceGit

class GitStore(AbstractStore):
  def __init__(self, store):
    self.__class__ = GitStore
    self.type = store

  def update_config(self, path, bare=False):
    self.path = path
    self.bare = bare

  def create(self, data):
    if data.__class__.__name__ == Workspace.__name__:
      wg = WorkspaceGit()
      wg.init(self.path, self.bare)

  def get(self):
    pass

  def store(self, store):
    pass
