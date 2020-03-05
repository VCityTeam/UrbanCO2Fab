from store.abstractstore import AbstractStore
from store.git.gitstore import GitStore
from store.nosql.nosqlstore import NosqlStore

class StoreFactory:
  def __init__(self):
    self._stores = {}
    nosqlstore = NosqlStore("nosql")
    gitstore = GitStore("git")
    self.add_store("nosql", nosqlstore)
    self.add_store("git", gitstore)

  def add_store(self, storetype, store):
    self._stores[storetype] = store
  
  def get_store(self, storetype):
    if storetype in self._stores:
      return self._stores[storetype]
    return None
