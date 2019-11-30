import numpy as np


class Node:
    def __init__(self, name, edges=None):
        self.name = name
        self.edges = {} if edges is None else edges

    def __repr__(self):
        return f'<Node with {len(self.edges)} edges>'

    def __str__(self):
        return f'Name: {self.name}\nConnections: {self.edges}'

    def add_connections(self, names, weights=None, on_conflict=np.mean):
        if weights is None:
            weights = [0 for _ in names]

        for n, w in zip(names, weights):
            name_exists = n in self.edges.keys()
            if name_exists and not on_conflict == 'overwrite':
                if callable(on_conflict):
                    self.edges[n] = on_conflict([self.edges[n], w])
                else:
                    raise KeyError('Connection already exists')
            else:
                self.edges[n] = w
