import sys
from collections import defaultdict

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

from util import read_input_as_lines


class Node:
    def __init__(self, name):
        self.name = name
        self.neighbours = set()

    def add_neighbour(self, node: 'Node'):
        assert isinstance(node, Node)
        self.neighbours.add(node)
        node.neighbours.add(self)

    def remove_neighbour(self, neighbour: 'Node'):
        assert isinstance(neighbour, Node)
        self.neighbours.remove(neighbour)
        neighbour.neighbours.remove(self)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name


def get_group_size_connected_to(node):
    group = {node}
    worklist = {node}
    seen = {node}
    while len(worklist) > 0:
        item: 'Node' = worklist.pop()
        seen.add(item)
        for nb in item.neighbours:
            group.add(nb)
            if nb not in seen:
                worklist.add(nb)
    return len(group)


def bridge_dfs(u, node: Node, count, low, pre, bridges):
    count += 1
    pre[node] = count
    low[node] = pre[node]
    for neighbour_node in node.neighbours:
        if pre[neighbour_node] == -1:
            bridge_dfs(node, neighbour_node, count, low, pre, bridges)
            low[node] = min(low[node], low[neighbour_node])
            if low[neighbour_node] == pre[neighbour_node]:
                bridges.append((node, neighbour_node))
        elif neighbour_node != u:
            low[node] = min(low[node], pre[neighbour_node])


def get_bridges(node_map):
    # Copied from stack overflow because I couldn't have done it better myself
    sys.setrecursionlimit(2000)
    bridges = []
    count = 0
    low = {n: -1 for n in node_map.values()}
    pre = low.copy()
    for node in node_map.values():
        bridge_dfs(node, node, count, low, pre, bridges)
    return bridges


def parse():
    lines = read_input_as_lines()
    node_map = {}
    for line in lines:
        key, value_str = line.split(': ')
        if key not in node_map:
            node_map[key] = Node(key)
        node: Node = node_map[key]
        neighbours = value_str.split(' ')
        for neighbour in neighbours:
            if neighbour not in node_map:
                node_map[neighbour] = Node(neighbour)
            node.add_neighbour(node_map[neighbour])
    return node_map


def do_dijkstra(node_map):
    indexed_node_list = list(node_map.values())
    distances = [([0] * len(indexed_node_list)) for _ in range(len(indexed_node_list))]
    for i, node in enumerate(indexed_node_list):
        for nb in node.neighbours:
            nb_index = indexed_node_list.index(nb)
            distances[i][nb_index] = 1
            distances[nb_index][i] = 1
    _, predecessors = dijkstra(csr_matrix(distances), return_predecessors=True)
    return indexed_node_list, predecessors


def make_edge_tuple(node_a, node_b):
    return tuple(sorted([node_a.name, node_b.name]))


def get_edge_in_betweenness(node_list, predecessor_matrix):
    edge_in_betweenness = defaultdict(int)
    for from_node_index in range(len(node_list)):
        for to_node_index in range(from_node_index + 1, len(node_list)):
            to_node = node_list[to_node_index]
            predecessor_index = predecessor_matrix[from_node_index][to_node_index]
            node_in_path = node_list[predecessor_index]
            edge_in_betweenness[make_edge_tuple(node_in_path, to_node)] += 1
            while from_node_index != predecessor_index:
                predecessor_index = predecessor_matrix[from_node_index][predecessor_index]
                next_node_in_path = node_list[predecessor_index]
                edge_in_betweenness[make_edge_tuple(node_in_path, next_node_in_path)] += 1
                node_in_path = next_node_in_path
    return edge_in_betweenness


def part1():
    node_map = parse()
    node_list, predecessors = do_dijkstra(node_map)

    edge_in_betweenness = get_edge_in_betweenness(node_list, predecessors)
    edges_to_try_ordered = sorted(edge_in_betweenness.keys(), key=lambda t: edge_in_betweenness[t], reverse=True)

    for i in range(len(edges_to_try_ordered)):
        name_i_a, name_i_b = edges_to_try_ordered[i]
        node_i_a, node_i_b = node_map[name_i_a], node_map[name_i_b]
        node_i_a.remove_neighbour(node_i_b)
        for j in range(i + 1, len(edges_to_try_ordered)):
            name_j_a, name_j_b = edges_to_try_ordered[j]
            node_j_a, node_j_b = node_map[name_j_a], node_map[name_j_b]
            node_j_a.remove_neighbour(node_j_b)
            bridges = get_bridges(node_map)
            if len(bridges) == 0:
                node_j_a.add_neighbour(node_j_b)
                continue
            assert len(bridges) == 1
            node_bridge_a, node_bridge_b = bridges[0]
            node_bridge_a.remove_neighbour(node_bridge_b)
            group_size = get_group_size_connected_to(node_bridge_a)
            return group_size * (len(node_map) - group_size)
        node_i_a.add_neighbour(node_i_b)
    assert False


def part2():
    pass


if __name__ == '__main__':
    res1 = part1()
    print(res1)
    assert res1 == 583632
    print(part2())
