from node import Node
from collections import OrderedDict


class Graph:
    def __init__(self):
        self.nodes = {}

    @property
    def _node_names(self):
        return [n.name for n in self.nodes]

    def add_nodes(self, names, edges=None):
        if edges is not None:
            for n, e in zip(names, edges):
                self.nodes[n] = Node(n, edges=e)
        else:
            for n in names:
                self.nodes[n] = Node(n)

    def add_connection(self, name_a, name_b, bi_directional=False, weight=0):
        if name_a not in self._node_names:
            self.add_nodes([name_a])

        if name_b not in self._node_names:
            self.add_nodes([name_b])

        self.nodes[name_a].add_connections([name_b], weight=weight)
        if bi_directional:
            self.nodes[name_b].add_connections([name_a], weight=weight)

    def merge(self, graph, agg_fun=sum):
        shared_keys = graph.nodes.keys() & self.nodes.keys()
        missing_keys = graph.nodes.keys() - self.nodes.keys()

        for k in shared_keys:
            self.nodes[k].add_connections(graph.nodes[k].edges.keys(),
                                          weights=graph.nodes[k].edges.values(),
                                          on_conflict=agg_fun)

        for k in missing_keys:
            self.nodes[k] = graph.nodes[k]

    def set_all_weights(self, value):
        for name, node in self.nodes.items():
            edges = node.edges
            node.edges = {}
            for k, _ in edges.items():
                node.edges[k] = value

            self.nodes[name] = node


if __name__ == '__main__':
    graph_1 = Graph()
    graph_2 = Graph()

    graph_1.add_nodes(['a', 'b'], edges=[{'b': 2}, {}])
    graph_2.add_nodes(['a', 'c'], edges=[{'b': 1}, {}])

    graph_1.merge(graph_2)
