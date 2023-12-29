from typing import Tuple, Set

from puzzles.Day23.Edge import Edge


class Node:
    def __init__(self, location: Tuple[int, int]):
        self.location: Tuple[int, int] = location
        self.edges: Set[Edge] = set()
        self.distance = {}

    def add_edge(self, to: 'Node'):
        edge = Edge(self, to)
        self.edges.add(edge)
        to.edges.add(edge)

    def get_neighbours(self):
        return [edge.get_neighbour(self) for edge in self.edges]

    def __hash__(self):
        return hash(self.location)

    def __repr__(self):
        return f'Node location={self.location} edges={self.edges}'
