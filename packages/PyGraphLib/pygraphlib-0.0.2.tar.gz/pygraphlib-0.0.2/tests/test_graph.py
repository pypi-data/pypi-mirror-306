import unittest
from PyGraphLib.module import Graph


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()

    # ------------------------------------------------------------------------
    # Tests init
    def test_init_with_dict_of_lists(self):
        graph_data = {
            "A": [("B", 1), ("C", 2)],
            "B": [("A", 1), ("C", 3)],
            "C": [("A", 2), ("B", 3)],
        }
        graph = Graph(graph=graph_data)
        expected_graph = {
            "A": {"B": [1], "C": [2]},
            "B": {"A": [1], "C": [3]},
            "C": {"A": [2], "B": [3]},
        }
        print("Actual Graph:", graph.graph)
        print("Expected Graph:", expected_graph)
        self.assertEqual(graph.graph, expected_graph)

    def test_init_with_dict_of_dicts(self):
        graph_data = {
            "A": {"B": 1, "C": 2},
            "B": {"A": 1, "C": 3},
            "C": {"A": 2, "B": 3},
        }
        graph = Graph(graph=graph_data)
        self.assertEqual(graph.graph, graph_data)

    def test_init_with_vertices_and_edges(self):
        V = {"A", "B", "C"}
        E = {("A", "B", 1), ("B", "C", 2), ("C", "A", 3)}
        graph = Graph(v=V, e=E)
        expected_graph = {"A": {"B": [1]}, "B": {"C": [2]}, "C": {"A": [3]}}
        self.assertEqual(graph.graph, expected_graph)

    def test_init_with_empty_graph(self):
        graph = Graph()
        self.assertEqual(graph.graph, {})

    # ------------------------------------------------------------------------
    # add edge
    def test_add_edge_directed(self):
        self.graph.add_edge("A", "B", weight=5, bidirected=False)
        self.assertIn("A", self.graph.graph)
        self.assertIn("B", self.graph.graph["A"])
        self.assertEqual(self.graph.graph["A"]["B"], [5])
        self.assertNotIn("B", self.graph.graph)
        self.assertNotIn("A", self.graph.graph.get("B", {}))

    def test_add_edge_bidirected(self):
        self.graph.add_edge("A", "B", weight=5, bidirected=True)
        self.assertIn("A", self.graph.graph)
        self.assertIn("B", self.graph.graph["A"])
        self.assertEqual(self.graph.graph["A"]["B"], [5])
        self.assertIn("B", self.graph.graph)
        self.assertIn("A", self.graph.graph["B"])
        self.assertEqual(self.graph.graph["B"]["A"], [5])

    def test_add_multiple_edges(self):
        self.graph.add_edge("A", "B", weight=5, bidirected=True)
        self.graph.add_edge("A", "B", weight=3, bidirected=True)
        self.assertEqual(self.graph.graph["A"]["B"], [5, 3])
        self.assertEqual(self.graph.graph["B"]["A"], [5, 3])

    def test_add_edge_existing_nodes(self):
        self.graph.graph = {"A": {"B": [2]}, "B": {"A": [2]}}
        self.graph.add_edge("A", "B", weight=5, bidirected=True)
        self.assertEqual(self.graph.graph["A"]["B"], [2, 5])
        self.assertEqual(self.graph.graph["B"]["A"], [2, 5])

    def test_add_edge_non_existing_nodes(self):
        self.graph.add_edge("A", "B", weight=5, bidirected=True)
        self.assertIn("A", self.graph.graph)
        self.assertIn("B", self.graph.graph)
        self.assertEqual(self.graph.graph["A"]["B"], [5])
        self.assertEqual(self.graph.graph["B"]["A"], [5])


if __name__ == "__main__":
    unittest.main()
