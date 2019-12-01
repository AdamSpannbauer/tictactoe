# TODO: finish documenting
import numpy as np
from node import Node


class Graph:
    """Represent a 'graph' of Node objects

    >>> graph = Graph()
    >>> graph.nodes
    """
    def __init__(self):
        self.nodes = {}

    @property
    def _node_names(self):
        return [n.name for n in self.nodes.values()]

    def add_nodes(self, names, edges=None):
        """Add Node objects and edges to graph

        :param names: list of node names to be added
        :param edges: list of edge dictionaries corresponding to the names arg
                      edges dict is expected to be of form `{node_name: edge_weight}`
        :return: None; nodes are added to `nodes` attribute

        >>> graph = Graph()
        >>> graph.nodes
        {}
        >>> graph.add_nodes(names=['a', 'b'])
        >>> graph.nodes
        {'a': <Node with 0 edges>, 'b': <Node with 0 edges>}
        >>> graph.nodes['a'].edges
        {}
        >>> graph = Graph()
        >>> graph.add_nodes(names=['a', 'b'], edges=[{'b': 5}, {}])
        >>> graph.nodes
        {'a': <Node with 1 edges>, 'b': <Node with 0 edges>}
        >>> graph.nodes['a'].edges
        {'b': 5}
        """
        if edges is not None:
            for n, e in zip(names, edges):
                self.nodes[n] = Node(n, edges=e)
        else:
            for n in names:
                self.nodes[n] = Node(n)

    def add_connection(self, name_a, name_b, bi_directional=False, weight=0, on_conflict=np.mean):
        # TODO: finish examples in this doc
        """

        :param name_a: name of left hand node as str
        :param name_b: name of right hand node as str
        :param bi_directional: should connections be added to both nodes? if False only added to left hand node
        :param weight: edge weight of given connection
        :param on_conflict: If connection of name already exists what should happen?
                             * If `on_conflict == 'overwrite'` then new weight replaces existing weight
                             * Elif `on_conflict` is a function, the old & new weights are passed as
                               a list to it (i.e. `on_conflict([old, new])`).
                             * Else a `KeyError` is `raise`d
        :return: None; `nodes` attribute is modified

        >>> graph = Graph()
        >>> graph.add_nodes(names=['a', 'b'])
        >>> graph.nodes
        {'a': <Node with 0 edges>, 'b': <Node with 0 edges>}
        >>> graph.add_connection('a', 'b', bi_directional=False, weight=5)
        >>> graph.nodes
        {'a': <Node with 1 edges>, 'b': <Node with 0 edges>}
        >>> graph.nodes['a'].edges
        {'b': 5}
        """
        if name_a not in self._node_names:
            self.add_nodes([name_a])

        if name_b not in self._node_names:
            self.add_nodes([name_b])

        self.nodes[name_a].add_connections([name_b], weights=[weight], on_conflict=on_conflict)
        if bi_directional:
            self.nodes[name_b].add_connections([name_a], weights=[weight], on_conflict=on_conflict)

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
