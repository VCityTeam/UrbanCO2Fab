from store.abstractstore import AbstractStore

class NosqlStore(AbstractStore):
  def __init__(self, store):
    self.__class__ = AbstractStore

  def create(self, data):
    pass

  def get(self):
    pass

  def store(self, store):
    pass
