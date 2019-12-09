import numpy as np
from .node import Node


class Graph:
    """Represent a 'graph' of Node objects

    >>> graph = Graph()
    >>> graph.nodes
    {}
    """
    def __init__(self):
        self.nodes = {}

    def __repr__(self):
        return f'<Graph with {len(self.nodes)} nodes>'

    @property
    def _node_names(self):
        return [n.name for n in self.nodes.values()]

    def _validate_graph(self, clean=False):
        """Check that all edges reference existing nodes

        :param clean: Should bad references be removed from the graph?
        :return: list of dictionaries showing bad references.  For example,
                 if node 'a' was referencing node 'c' which didn't exist the
                 output would be: `[{'node': 'a', 'bad_ref': 'c'}]`

        >>> graph = Graph()
        >>> graph.add_connection('a', 'b', bi_directional=True)
        >>> graph.nodes['a'].add_connections(names=['c'])
        >>> graph.nodes['a'].edges
        {'b': 0, 'c': 0}
        >>> # noinspection PyProtectedMember
        >>> invalid_references = graph._validate_graph(clean=True)
        >>> invalid_references
        [{'node': 'a', 'bad_ref': 'c'}]
        >>> graph.nodes['a'].edges
        {'b': 0}
        """
        bad_refs = []
        for node_a in self._node_names:
            for node_b in self.nodes[node_a].edges.keys():
                if node_b not in self._node_names:
                    bad_refs.append({'node': node_a, 'bad_ref': node_b})

        if clean:
            for bad_ref in bad_refs:
                self.remove_connection(bad_ref['node'], bad_ref['bad_ref'])

        return bad_refs

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

    def remove_nodes(self, names, rm_edges=True):
        """Delete nodes from the graph

        :param names: list of node names to be deleted
        :param rm_edges: remove edges that reference nodes to be deleted
        :return: None; `nodes` attribute is modified

        >>> graph = Graph()
        >>> graph.add_nodes(['a', 'b', 'c'])
        >>> graph
        <Graph with 3 nodes>
        >>> graph.remove_nodes(['a', 'b'])
        >>> graph.nodes
        {'c': <Node with 0 edges>}
        >>> graph = Graph()
        >>> graph.add_nodes(['a', 'b', 'c'], [{'b': 1}, {}, {}])
        >>> graph.remove_nodes(['b', 'c'])
        >>> graph.nodes['a'].edges
        {}
        >>> graph = Graph()
        >>> graph.add_nodes(['a', 'b', 'c'], [{'b': 1}, {}, {}])
        >>> graph.remove_nodes(['b', 'c'], rm_edges=False)
        >>> graph.nodes['a'].edges
        {'b': 1}
        """
        for name in names:
            self.nodes.pop(name, None)

        if rm_edges:
            self._validate_graph(clean=True)

    def add_connection(self, name_a, name_b, bi_directional=False, weight=0, on_conflict=np.mean):
        """Add edge(s) to the graph

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
        >>> graph.add_connection('a', 'b', weight=5)
        >>> graph.nodes
        {'a': <Node with 1 edges>, 'b': <Node with 0 edges>}
        >>> graph.nodes['a'].edges
        {'b': 5}
        >>> graph.add_connection('b', 'a', weight=5)
        >>> graph.nodes
        {'a': <Node with 1 edges>, 'b': <Node with 1 edges>}
        >>> graph.nodes['b'].edges
        {'a': 5}
        >>> graph = Graph()
        >>> graph.add_nodes(names=['a', 'b'])
        >>> graph.add_connection('a', 'b', bi_directional=True, weight=5)
        >>> graph.nodes
        {'a': <Node with 1 edges>, 'b': <Node with 1 edges>}
        >>> graph.nodes['b'].edges
        {'a': 5}
        """
        if name_a not in self._node_names:
            self.add_nodes([name_a])

        if name_b not in self._node_names:
            self.add_nodes([name_b])

        self.nodes[name_a].add_connections([name_b], weights=[weight], on_conflict=on_conflict)
        if bi_directional:
            self.nodes[name_b].add_connections([name_a], weights=[weight], on_conflict=on_conflict)

    def remove_connection(self, name_a, name_b, bi_directional=False):
        """Remove edge(s) from the graph

        :param name_a: name of left hand node as str
        :param name_b: name of right hand node as str
        :param bi_directional: should connections be removed from both nodes? if False only removed from left hand node
        :return: None; `nodes` attribute is modified

        >>> graph = Graph()
        >>> graph.add_nodes(names=['a', 'b'], edges=[{'b': 10}, {'a': 5}])
        >>> graph.nodes
        {'a': <Node with 1 edges>, 'b': <Node with 1 edges>}
        >>> graph.remove_connection('a', 'b')
        >>> graph.nodes
        {'a': <Node with 0 edges>, 'b': <Node with 1 edges>}
        >>> graph.remove_connection('b', 'a')
        >>> graph.nodes
        {'a': <Node with 0 edges>, 'b': <Node with 0 edges>}
        >>> graph.add_nodes(names=['a', 'b'], edges=[{'b': 10}, {'a': 5}])
        >>> graph.nodes
        {'a': <Node with 1 edges>, 'b': <Node with 1 edges>}
        >>> graph.remove_connection('a', 'b', bi_directional=True)
        >>> graph.nodes
        {'a': <Node with 0 edges>, 'b': <Node with 0 edges>}
        """
        self.nodes[name_a].remove_connections([name_b])
        if bi_directional:
            self.nodes[name_b].remove_connections([name_a])

    def merge(self, graph, agg_fun=sum):
        """Add the nodes & edges of another Graph object

        :param graph: A Graph object to be merged into this one.
        :param agg_fun: Function that accepts a list of numbers as input and outputs a single numeric value.
                        Will be used to aggregate common edges between the 2 graphs.
                        For example, in graph 1 there exists A--5-->B and in graph 2 there exists A --3--> B.
                        If `sum` is the agg_fun, then the resulting merged graph will have A --8--> B.
        :return: None; `nodes` attribute is modified

        >>> graph_1 = Graph()
        >>> graph_2 = Graph()
        >>> graph_1.add_nodes(['a', 'b'], edges=[{'b': 5}, {}])
        >>> graph_2.add_nodes(['a', 'c'], edges=[{'b': 3}, {}])
        >>> graph_1.merge(graph_2)
        >>> graph_1
        <Graph with 3 nodes>
        >>> graph_1.nodes['a'].edges['b']
        8
        """
        shared_keys = graph.nodes.keys() & self.nodes.keys()
        missing_keys = graph.nodes.keys() - self.nodes.keys()

        for k in shared_keys:
            self.nodes[k].add_connections(graph.nodes[k].edges.keys(),
                                          weights=graph.nodes[k].edges.values(),
                                          on_conflict=agg_fun)

        for k in missing_keys:
            self.nodes[k] = graph.nodes[k]

    def set_all_weights(self, value):
        """Set every edge weight in the graph to a certain value

        :param value: value to set all edge weights to
        :return: None; `nodes` attribute is modified

        >>> graph = Graph()
        >>> graph.add_nodes(['a', 'b', 'c'], [{'b': 0, 'c': 1}, {'a': 2}, {}])
        >>> graph.nodes['a'].edges
        {'b': 0, 'c': 1}
        >>> graph.set_all_weights(-1)
        >>> graph.nodes['a'].edges
        {'b': -1, 'c': -1}
        >>> graph.nodes['b'].edges
        {'a': -1}
        >>> graph.nodes['c'].edges
        {}
        """
        for name, node in self.nodes.items():
            edges = node.edges
            node.edges = {}
            for k in edges.keys():
                node.edges[k] = value

            self.nodes[name] = node
