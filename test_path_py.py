import unittest
from path import Path, finding_shortest_path, highlight_path
from graph import Graph, Node, AddNode, AddSegment, SearchNode


class TestPath(unittest.TestCase):
    def setUp(self):

        self.graph = Graph()

        AddNode(self.graph, Node("A", 1, 1))
        AddNode(self.graph, Node("B", 2, 2))
        AddNode(self.graph, Node("C", 3, 3))
        AddNode(self.graph, Node("D", 4, 4))
        AddNode(self.graph, Node("E", 5, 5))


        AddSegment(self.graph, "AB", "A", "B", cost=1)
        AddSegment(self.graph, "BC", "B", "C", cost=2)
        AddSegment(self.graph, "CD", "C", "D", cost=3)
        AddSegment(self.graph, "AD", "A", "D", cost=10)  # Direct but expensive
        AddSegment(self.graph, "DE", "D", "E", cost=1)
        AddSegment(self.graph, "AE", "A", "E", cost=100)  # Very expensive direct path

    def test_path_creation(self):

        node_a = SearchNode(self.graph, "A")
        node_b = SearchNode(self.graph, "B")

        path = Path("test_path", node_a, node_b, 5)
        self.assertEqual(path.name, "test_path")
        self.assertEqual(path.origin, node_a)
        self.assertEqual(path.destination, node_b)
        self.assertEqual(path.cost, 5)
        self.assertEqual(path.nodes, [node_a])
        self.assertEqual(path.segments, [])

    def test_add_node_to_path(self):

        node_a = SearchNode(self.graph, "A")
        node_b = SearchNode(self.graph, "B")
        segment_ab = next(s for s in self.graph.segments if s.name == "AB")

        path = Path("test_path", node_a)
        path.AddNodeToPath(node_b, segment_ab)

        self.assertEqual(path.nodes, [node_a, node_b])
        self.assertEqual(path.segments, [segment_ab])
        self.assertEqual(path.cost, segment_ab.cost)
        self.assertEqual(path.destination, node_b)

    def test_contains_node(self):

        node_a = SearchNode(self.graph, "A")
        node_b = SearchNode(self.graph, "B")
        node_c = SearchNode(self.graph, "C")

        path = Path("test_path", node_a)
        path.AddNodeToPath(node_b, next(s for s in self.graph.segments if s.name == "AB"))

        self.assertTrue(path.ContainsNode(node_a))
        self.assertTrue(path.ContainsNode(node_b))
        self.assertFalse(path.ContainsNode(node_c))

    def test_cost_to_node(self):

        node_a = SearchNode(self.graph, "A")
        node_b = SearchNode(self.graph, "B")
        node_c = SearchNode(self.graph, "C")
        segment_ab = next(s for s in self.graph.segments if s.name == "AB")
        segment_bc = next(s for s in self.graph.segments if s.name == "BC")

        path = Path("test_path", node_a)
        path.AddNodeToPath(node_b, segment_ab)
        path.AddNodeToPath(node_c, segment_bc)

        self.assertEqual(path.CostToNode(node_a), 0)
        self.assertEqual(path.CostToNode(node_b), segment_ab.cost)
        self.assertEqual(path.CostToNode(node_c), segment_ab.cost + segment_bc.cost)
        self.assertEqual(path.CostToNode(SearchNode(self.graph, "D")), -1)

    def test_find_shortest_path_simple(self):

        node_a = SearchNode(self.graph, "A")
        node_b = SearchNode(self.graph, "B")

        path = finding_shortest_path(self.graph, node_a, node_b)

        self.assertIsNotNone(path)
        self.assertEqual(path.origin, node_a)
        self.assertEqual(path.destination, node_b)
        self.assertEqual(path.cost, 1)
        self.assertEqual(len(path.nodes), 2)
        self.assertEqual(len(path.segments), 1)

    def test_find_shortest_path_complex(self):

        node_a = SearchNode(self.graph, "A")
        node_d = SearchNode(self.graph, "D")

        path = finding_shortest_path(self.graph, node_a, node_d)

        self.assertIsNotNone(path)
        self.assertEqual(path.origin, node_a)
        self.assertEqual(path.destination, node_d)

        self.assertEqual(path.cost, 6)
        self.assertEqual(len(path.nodes), 4)
        self.assertEqual(len(path.segments), 3)

    def test_find_shortest_path_no_path(self):

        AddNode(self.graph, Node("Z", 10, 10))
        node_a = SearchNode(self.graph, "A")
        node_z = SearchNode(self.graph, "Z")

        path = finding_shortest_path(self.graph, node_a, node_z)

        self.assertIsNone(path)

    def test_highlight_path(self):

        node_a = SearchNode(self.graph, "A")
        node_e = SearchNode(self.graph, "E")

        path = finding_shortest_path(self.graph, node_a, node_e)
        try:
            highlight_path(path)
            # If we get here without exceptions, it's a success
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"highlight_path raised exception: {e}")

    def test_find_shortest_path_same_node(self):

        node_a = SearchNode(self.graph, "A")

        path = finding_shortest_path(self.graph, node_a, node_a)

        self.assertIsNotNone(path)
        self.assertEqual(path.origin, node_a)
        self.assertEqual(path.destination, node_a)
        self.assertEqual(path.cost, 0)
        self.assertEqual(len(path.nodes), 1)
        self.assertEqual(len(path.segments), 0)


if __name__ == '__main__':
    unittest.main()