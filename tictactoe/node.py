import numpy as np


class Node:
    """Represent 'nodes' in a Graph

    :param name: name of node (must be a data type allowed to be a dict key)
    :param edges: dictionary of 'edges' of format `{node_name: edge_weight}`
    :ivar name: name of node
    :ivar edges: dictionary of 'edges' of format `{node_name: edge_weight}`

    >>> a = Node('a')
    >>> b = Node('b', edges={'c': 4})
    >>> a
    <Node with 0 edges>
    >>> b
    <Node with 1 edges>
    >>> a.edges
    {}
    >>> b.edges
    {'c': 4}
    """
    def __init__(self, name, edges=None):
        self.name = name
        self.edges = {} if edges is None else edges

    def __repr__(self):
        return f'<Node with {len(self.edges)} edges>'

    def __str__(self):
        return f'Name: {self.name}\nConnections: {self.edges}'

    def add_connections(self, names, weights=None, on_conflict=np.mean):
        """Add connections to other Nodes

        :param names: list of node names to connect to
        :param weights: list of weights for connections (order corresponds to names param)
        :param on_conflict: If connection of name already exists what should happen?
                             * If `on_conflict == 'overwrite'` then new weight replaces existing weight
                             * Elif `on_conflict` is a function, the old & new weights are passed as
                               a list to it (i.e. `on_conflict([old, new])`).
                             * Else a `KeyError` is `raise`d
        :return: None; edges are added to `edges` attribute

        >>> a = Node('a')
        >>> a.add_connections(names=['b', 'c'])
        >>> a.edges
        {'b': 0, 'c': 0}
        >>> a.add_connections(names=['d', 'e'], weights=[10, -1])
        >>> a.edges
        {'b': 0, 'c': 0, 'd': 10, 'e': -1}
        >>> a = Node('a', edges={'b': 0})
        >>> a.edges
        {'b': 0}
        >>> a.add_connections(names=['b'], weights=[5], on_conflict='overwrite')
        >>> a.edges
        {'b': 5}
        >>> a.add_connections(names=['b'], weights=[5], on_conflict=np.sum)
        >>> a.edges
        {'b': 10}
        >>> # a.add_connections(names=['b'], weights=[5], on_conflict='fail')
        KeyError: 'Connection already exists'
        """
        if weights is None:
            weights = [0 for _ in names]

        for name, weight in zip(names, weights):
            name_exists = name in self.edges.keys()
            if name_exists and not on_conflict == 'overwrite':
                if callable(on_conflict):
                    self.edges[name] = on_conflict([self.edges[name], weight])
                else:
                    raise KeyError('Connection already exists')
            else:
                self.edges[name] = weight

    def remove_connections(self, names):
        """Remove connections from edges attribute by list of names

        :param names: list of node names corresponding to edges to remove.
                      Doesn't throw exception if name doesn't exist
        :return: None; edges are removed from `edges` attribute

        >>> a = Node('a', {'b': 1, 'c': 2, 'd': 3})
        >>> a.remove_connections(['c', 'd'])
        >>> a.edges
        {'b': 1}
        >>> a.remove_connections(['b', 'fake'])
        >>> a.edges
        {}
        """
        for name in names:
            self.edges.pop(name, None)
