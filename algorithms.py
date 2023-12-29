from functools import reduce


def dijkstra(start_node, get_neighbours_of_node, get_cost_of_node):
    visited = set()
    to_visit = set()
    distances = {start_node: 0}
    paths = {start_node: []}
    node = start_node
    while True:
        current_distance = distances[node]
        current_path = paths[node]
        neighbours = set(get_neighbours_of_node(node))
        for neighbour in neighbours:
            known_distance = distances.get(neighbour)
            distance_via_current = current_distance + get_cost_of_node(neighbour)
            if known_distance is None or distance_via_current < known_distance:
                distances[neighbour] = distance_via_current
                paths[neighbour] = current_path + [neighbour]
        visited.add(node)
        to_visit = to_visit.union(neighbours).difference(visited)
        if len(to_visit) == 0:
            return distances, paths
        node = min(to_visit, key=lambda t: distances[t])


def dijkstra_distance(start_node, get_neighbours_of_node, get_cost_of_node):
    visited = set()
    to_visit = set()
    distances = {start_node: 0}
    node = start_node
    while True:
        current_distance = distances[node]
        neighbours = set(get_neighbours_of_node(node))
        for neighbour in neighbours:
            known_distance = distances.get(neighbour)
            distance_via_current = current_distance + get_cost_of_node(neighbour)
            if known_distance is None or distance_via_current < known_distance:
                distances[neighbour] = distance_via_current
        visited.add(node)
        to_visit = to_visit.union(neighbours).difference(visited)
        if len(to_visit) == 0:
            return distances
        node = min(to_visit, key=lambda t: distances[t])


def chinese_remainder(m, a):
    s = 0
    prod = reduce(lambda acc, b: acc * b, m)
    for n_i, a_i in zip(m, a):
        p = prod // n_i
        s += a_i * mul_inv(p, n_i) * p
    return s % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1
