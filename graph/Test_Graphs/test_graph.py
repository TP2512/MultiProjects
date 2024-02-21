import unittest
from Graph_Processing.graph_creation import Graphs

class TestGraph(unittest.TestCase):
    def setUp(self):
        # Initialize a new Graph instance before each test
        self.graph = Graphs()

    def test_add_edge(self):
        self.graph.add_edge('A', 'B')
        self.graph.add_edge('B', 'F')
        self.graph.add_edge('F', 'G')
        self.graph.add_edge('G', 'H')
        self.graph.add_edge('H', 'A')
        self.assertIn('B', self.graph['A'])
        self.assertIn('A', self.graph['B'])
        self.assertNotIn('C', self.graph['A'])
        self.assertIn('H', self.graph['A'])
        self.graph.remove_node('H')
        self.assertNotIn('H', self.graph['A'])
        self.assertIn('B', self.graph['A'])
        self.graph.remove_edge(('B','A'))
        self.assertEqual(self.graph['A'],set())

    def test_getitem(self):
        self.graph.add_edge('B', 'A')
        self.graph.add_edge('H', 'G')
        self.graph.add_edge('F', 'B')
        self.graph.add_edge('F', 'G')
        self.graph.add_edge('H', 'A')
        self.assertEqual(self.graph['A'], {'H','B'})
        # print(self.graph['A'])
        self.assertNotEqual(self.graph['B'], set())  # Ensure that 'B' has no outgoing edges



if __name__ == '__main__':
    unittest.main()
