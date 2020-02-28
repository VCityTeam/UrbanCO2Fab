from urbanco2fab.store.abstractstore import AbstractStore

class GitStore(AbstractStore):
  @abstractmethod
  def __init__(self, store):
    self.__class__ = AbstractStore

  @abstractmethod
  def create(self, data):
    pass

  @abstractmethod
  def get(self):
    pass

  @abstractmethod
  def store(self, store):
    pass
