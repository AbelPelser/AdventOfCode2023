from functools import cache

from puzzles.Day23.Edge import Edge
from puzzles.Day23.Node import Node
from util import read_input_as_lines, enumerate_matrix

DELTAS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


@cache
def is_in_bounds(grid, x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])


@cache
def get_up_right_neighbours(grid, x, y):
    result = set()
    for dx, dy in {(-1, 0), (0, -1)}:
        nx, ny = x + dx, y + dy
        if is_in_bounds(grid, nx, ny):
            result.add((nx, ny))
    return result


def make_nodes(grid_):
    nodes = {}
    for (y, x), char in enumerate_matrix(grid_):
        if char == '#':
            continue
        coord = (x, y)
        node = Node(coord)
        for (nx, ny) in get_up_right_neighbours(grid_, x, y):
            if grid_[ny][nx] != '#':
                node.add_edge(nodes[(nx, ny)])
        nodes[(x, y)] = node
    return nodes


def reduce_node_map(node_map, start, goal):
    node_items = set(node_map.items())
    changed = False
    start_node = node_map[start]
    goal_node = node_map[goal]
    for coord, node in node_items:
        if len(node.edges) == 1 and node != start_node and node != goal_node:
            edge = list(node.edges)[0]
            other = edge.get_neighbour(node)
            other.edges.remove(edge)
            del node_map[coord]
            changed = True
        elif len(node.edges) == 2:
            first_edge, second_edge = node.edges
            first_neighbour: Node = first_edge.get_neighbour(node)
            second_neighbour: Node = second_edge.get_neighbour(node)
            new_edge: Edge = Edge(first_neighbour, second_neighbour)
            new_edge.length = first_edge.length + second_edge.length
            first_neighbour.edges.remove(first_edge)
            second_neighbour.edges.remove(second_edge)
            first_neighbour.edges.add(new_edge)
            second_neighbour.edges.add(new_edge)
            del node_map[coord]
            changed = True
    return changed


@cache
def has_path_to_goal(node, seen, goal_node):
    if node == goal_node:
        return True
    seen = set(seen)
    for edge in node.edges:
        neighbour = edge.get_neighbour(node)
        assert neighbour != node
        if neighbour == goal_node:
            return True
        if neighbour in seen:
            continue
        seen.add(neighbour)
        if has_path_to_goal(neighbour, tuple(seen), goal_node):
            seen.remove(neighbour)
            return True
        seen.remove(neighbour)
    return False


def tmp_recursive(distance: int, node: Node, seen: set, goal_node):
    to_visit = []
    for edge in node.edges:
        neighbour = edge.get_neighbour(node)
        if neighbour in seen:
            continue
        next_distance = distance + edge.length
        if neighbour == goal_node:
            return next_distance
        to_visit.append((next_distance, neighbour))
    to_visit.sort(key=lambda t: sum(t[1].location))
    best_sub_result = 0
    for args in to_visit:
        next_distance, neighbour = args
        seen.add(neighbour)
        if not has_path_to_goal(neighbour, tuple(seen), goal_node):
            seen.remove(neighbour)
            continue
        sub_result = tmp_recursive(next_distance, neighbour, seen, goal_node)
        seen.remove(neighbour)
        if sub_result > best_sub_result:
            best_sub_result = sub_result
    return best_sub_result


def part1():
    pass


def part2():
    lines = read_input_as_lines()
    grid = list(map(list, lines))
    grid = tuple(tuple(l) for l in grid)
    goal = (len(grid[-1]) - 2, len(grid) - 1)

    nodes_map = make_nodes(grid)
    keep_going = reduce_node_map(nodes_map, (1, 0), goal)
    while keep_going:
        keep_going = reduce_node_map(nodes_map, (1, 0), goal)

    return tmp_recursive(0, nodes_map[(1, 0)], set(), nodes_map[goal])


if __name__ == '__main__':
    print(part1())
    print(part2())
