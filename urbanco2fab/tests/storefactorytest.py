import unittest

from store.storefactory import StoreFactory
from store.git.gitstore import GitStore
from store.nosql.nosqlstore import NosqlStore

class StoreFactoryTestSuite(unittest.TestCase):
  def test_basic_storefactory(self):
     sf = StoreFactory()
     self.assertEqual(type(sf.get_store("git")), type(GitStore))
     self.assertEqual(type(sf.get_store("nosql")), type(NosqlStore))

if __name__ == '__main__':
  unittest.main()
