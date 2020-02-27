from git.gitstore import GitStore
from nosql.nosqlstore import NosqlStore

class StoreFactory:
  def __init__():
    self._stores = {}

  def add_store(self, storetype, store):
    self._stores[storetype] = store
  
  def get_store(self, storetype):
    if storetype in self.__store:
      return self._store[storetype]
    return None
        
