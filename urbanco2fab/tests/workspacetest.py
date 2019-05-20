import unittest
import sys
sys.path.append("../")

from workspace import Workspace


class WorkspaceTestSuite(unittest.TestCase):
  def test_constant(self):
    workspace = Workspace("workspace.json")
    self.assertEqual(workspace.get_identifier(), "official workspace")
    self.assertEqual(workspace.get_consensus_scenario(), "First")
    self.assertEqual(workspace.get_proposition_scenarios(), ['Second', 'Third'])
    self.assertEqual(workspace.get_influence_transitions(), ['70256c32c6f15b233a0ee84b85116df218229df8:dc3872a240d8edd6b07142a2b5dbd4b1c4d12985'])

if __name__ == '__main__':
  unittest.main()
