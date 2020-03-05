from store.abstractstore import AbstractStore
from store.git.gitstore import GitStore
from store.nosql.nosqlstore import NosqlStore

class StoreFactory:
  def __init__(self):
    self._stores = {}
    self.add_store("nosql", NosqlStore)
    self.add_store("git", GitStore)

  def add_store(self, storetype, store):
    for base in store.__bases__:
      if (base.__name__ == AbstractStore.__name__):
        self._stores[storetype] = store
  
  def get_store(self, storetype):
    if storetype in self._stores:
      return self._stores[storetype]
    return None
