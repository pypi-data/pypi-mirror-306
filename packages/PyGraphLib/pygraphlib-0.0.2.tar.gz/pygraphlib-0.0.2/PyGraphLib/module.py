import matplotlib.pyplot as plt
import random
from copy import deepcopy
from itertools import combinations

AdjacencyList = dict[str, dict[str, list[int]]]
Distances = dict[str, float]
Predecessors = dict[str, str]


def _create_path(start: str, graph: AdjacencyList):
    path: list[str] = []

    def dfs(curr: str):
        while graph.get(curr):
            next_node = next(iter(graph[curr]))
            # Remove edge between curr and next_node
            if next_node in graph[curr]:
                if len(graph[curr][next_node]) > 1:
                    graph[curr][next_node].pop()
                else:
                    del graph[curr][next_node]
            if curr in graph[next_node]:
                if len(graph[next_node][curr]) > 1:
                    graph[next_node][curr].pop()
                else:
                    del graph[next_node][curr]
            dfs(next_node)
        path.append(curr)

    dfs(start)
    return path[::-1]


class Graph:
    graph: AdjacencyList

    def __init__(self, graph: dict = {}, v: set = set(), e: set = set()) -> None:
        # detect graph type
        if graph != {} and type(graph[list(graph.keys())[0]]) is list:
            # "A": [("B", 1), ("C", 2)],
            self.graph = {k: {v[0]: [v[1]] for v in graph[k]} for k in graph}
        elif graph != {} and type(graph[list(graph.keys())[0]]) is dict:
            self.graph = graph
        elif v != set() and e != set() and type(v) is set and type(e) is set:
            # flo type
            self.graph = {vertex: {} for vertex in v}
            for edge in e:
                start, end, weight = edge if len(edge) == 3 else (*edge, 1)
                self.graph[start][end] = [weight]
        else:
            self.graph = {}

    def add_edge(
        self,
        origin: str,
        to: str,
        weight=1,
        bidirected=True,
    ):
        if (
            origin in self.graph
            and to in self.graph
            and to in self.graph[origin]
            and origin in self.graph[to]
        ):
            return
        if origin not in self.graph:
            self.graph[origin] = {}
        if to not in self.graph and bidirected:
            self.graph[to] = {}

        if to not in self.graph[origin]:
            self.graph[origin][to] = []
        if origin not in self.graph[to] and bidirected:
            self.graph[to][origin] = []

        self.graph[origin][to].append(weight)
        if bidirected:
            self.graph[to][origin].append(weight)

    def remove_edge(self, origin: str, to: str, all=True):
        if not all:
            raise NotImplementedError("Not implemented yet")
        if origin in self.graph and to in self.graph:
            del self.graph[origin][to]
            del self.graph[to][origin]

    def update_edge(self, origin: str, to: str, weight: int, index: int = 0):
        if origin in self.graph and to in self.graph:
            if len(self.graph[origin][to]) >= index:
                self.graph[origin][to][index] = weight
                self.graph[to][origin][index] = weight
            else:
                print(
                    f"attempted to update non existing edge {origin}-{to} to value {weight}"
                )

    def get_distance_between(self, origin: str, to: str) -> float:
        dists, _ = self.dijkstra(origin)
        return dists[to]

    def get_path_between(self, origin: str, to: str) -> list:
        _, preds = self.dijkstra(origin)

        path: list[str] = [to]
        last: str = to
        while preds[last] != "":
            last = preds[last]
            path.append(last)

        return list(reversed(path))

    def find_perfect_matching(self) -> "Graph":
        matchings: list[Graph] = []

        def create_matchings(matching: Graph, used_nodes: set):
            if len(used_nodes) == len(self.graph):
                # matching found
                matchings.append(deepcopy(matching))
                return

            # Find first unused node
            for u in self.graph:
                if u not in used_nodes:
                    break

            # match u with every possible neighbor
            for v in self.graph[u]:
                if v not in used_nodes:
                    # Add edge (u, v) to the current matching
                    matching.add_edge(u, v, self.graph[u][v][0])
                    used_nodes.update({u, v})

                    # search further with new node added
                    create_matchings(matching, used_nodes)

                    # Backtrack: remove (u, v) and reset used nodes
                    matching.remove_edge(u, v)
                    used_nodes.remove(u)
                    used_nodes.remove(v)

        create_matchings(Graph(), set())

        # find matching with minimal cost
        perfect_matching = min(
            (
                (
                    matching,
                    sum(
                        sum(v[0] for v in matching.graph[u].values())
                        for u in matching.graph
                    ),
                )
                for matching in matchings
            ),
            key=lambda x: x[1],
            default=(Graph(), float("Inf")),
        )

        print(f"perfect: {perfect_matching[0].graph}")
        return perfect_matching[0]

    def dijkstra(self, start: str) -> tuple[Distances, Predecessors]:
        assert start != "", "start cannot be empty"

        distances: dict[str, float] = {node: float("infinity") for node in self.graph}
        distances[start] = 0

        visited = set()
        nodes_to_visit: list[tuple[str, float]] = [(start, 0)]

        while nodes_to_visit:
            # Find vertex with the smallest distance
            current_v, current_dist = None, float("infinity")
            for node, dist in nodes_to_visit:
                if dist < current_dist and node not in visited:
                    current_v, current_dist = node, dist

            # break if there are no more vertecies to visit
            if current_v is None:
                break

            # Remove current_node from nodes_to_visit and mark it as visited
            nodes_to_visit = [n for n in nodes_to_visit if n[0] != current_v]
            visited.add(current_v)

            # Update distances to each neighbor
            for neighbor in self.graph[current_v]:
                distance = current_dist + self.graph[current_v][neighbor][0]

                # found shorter path to neighbor
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    nodes_to_visit.append((neighbor, distance))

        # get predecessors
        predecessors: dict[str, str] = {v: "" for v in self.graph}
        for node, distance in distances.items():
            for neighbor in self.graph[node]:
                if distances[neighbor] == distance + self.graph[node][neighbor][0]:
                    predecessors[neighbor] = node

        return distances, predecessors

    def get_spt(self, start: str, preds: Predecessors = {}, dists: Distances = {}):
        distances, predecessors = (
            self.dijkstra(start) if preds == {} and dists == {} else (dists, preds)
        )

        spt: dict[str, dict[str, float]] = {k: {} for k in predecessors.keys()}
        for node in predecessors.keys():
            pred = predecessors[node]
            if pred == "":
                continue
            spt[pred][node] = distances[node]
        return {k: spt[k] for k in spt.keys() if spt[k] != {}}

    def plot_spt(self, coords, start):
        def normalize(coords: dict[str, tuple[int, int]]):
            max_x, max_y = 0, 0
            for k in coords:
                max_x = max_x if coords[k][0] < max_x else coords[k][0]
                max_y = max_y if coords[k][1] < max_y else coords[k][1]

            return {
                k: (coords[k][0] / max_x, (max_y - coords[k][1]) / max_y)
                for k in coords
            }

        norm = normalize(coords)

        spt = self.get_spt(start)

        for k in norm:
            plt.text(norm[k][0], norm[k][1], k)

        # plot base graph in grey with edge weights
        for k in self.graph:
            for e in self.graph[k]:
                plt.plot(
                    [norm[k][0], norm[e][0]],
                    [norm[k][1], norm[e][1]],
                    "grey",
                    label="gorg",
                )
                plt.text(
                    (norm[k][0] + norm[e][0]) / 2,
                    (norm[k][1] + norm[e][1]) / 2,
                    self.graph[k][e],
                    color="grey",
                )

        # overlay shortest path in red
        for k in spt:
            for e in spt[k]:
                weight = spt[k][e]
                plt.plot([norm[k][0], norm[e][0]], [norm[k][1], norm[e][1]], "ro-")
                plt.text(
                    norm[e][0],
                    norm[e][1] - 0.03,
                    weight,
                    color="blue",
                )

        from matplotlib.lines import Line2D

        grey_line = Line2D([], [], color="grey", label="Base Graph")
        red_line = Line2D([], [], color="red", label="Shortest Paths")
        blue_text = Line2D([], [], color="blue", label="Sum of Weight")
        plt.legend(handles=[grey_line, red_line, blue_text])
        plt.show()
        pass

    # has eulerian path
    def hierholzner(self) -> list[str]:
        self.tmp_graph = {k: self.graph[k] for k in self.graph}
        # find num odd nodes and starting node
        num_odd_nodes = 0
        start_node = ""
        for node in self.graph:
            if len(self.graph[node]) % 2 != 0:
                num_odd_nodes += 0
                start_node = node

        num_odd_nodes = sum(
            [
                len([v for val in self.graph[node].values() for v in val]) % 2
                for node in self.graph
            ]
        )

        if num_odd_nodes != 0 and num_odd_nodes != 2:
            return []

        if num_odd_nodes == 0:
            start_idx = random.randrange(0, len(self.graph.keys()))  # or always 0
            start_node = list(self.graph.keys())[start_idx]

        path: list[str] = []
        path.extend(_create_path(start_node, self.tmp_graph))
        print(path)
        while True:
            for node in path:
                if len(self.tmp_graph.get(node, {})) > 0:
                    sub = _create_path(node, self.tmp_graph)
                    print(path)
                    path.extend(sub)

            can_exit = True
            for node in self.tmp_graph:
                if len(self.tmp_graph[node].keys()) > 0:
                    can_exit = False
            if can_exit:
                break

        return path

    def chinese_postman(self) -> list[str]:
        # get odd nodes
        odd_nodes: list[str] = []
        for node in self.graph:
            if len(self.graph[node]) % 2 != 0:
                odd_nodes.append(node)

        # complete graph
        comp_graph = Graph()
        for u, v in combinations(odd_nodes, 2):
            comp_graph.add_edge(u, v)

        # get distances
        for node in comp_graph.graph:
            for node2 in comp_graph.graph[node]:
                distance = self.get_distance_between(node, node2)
                comp_graph.add_edge(node, node2, distance)

        # perfect matching
        perfect_m = comp_graph.find_perfect_matching()

        # double vertex length from perfect matching in original graph
        new_graph = deepcopy(self)
        for u in perfect_m.graph:
            for v in perfect_m.graph[u]:
                path: list[str] = self.get_path_between(u, v)
                for node_idx in range(len(path) - 1):
                    new_graph.graph[path[node_idx]][path[node_idx + 1]] = [
                        new_graph.graph[path[node_idx]][path[node_idx + 1]][0],
                        new_graph.graph[path[node_idx]][path[node_idx + 1]][0],
                    ]

        return new_graph.hierholzner()
    
if __name__ == "__main__":
    graph_data = {
        "A": [("B", 1), ("C", 2)],
        "B": [("A", 1), ("C", 3)],
        "C": [("A", 2), ("B", 3)],
    }
    graph = Graph(graph=graph_data)
    print(graph.graph)
