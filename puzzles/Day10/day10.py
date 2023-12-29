from collections import defaultdict
from typing import List, Tuple, Dict, Set

from util import read_input_as_lines, enumerate_matrix

DELTA_MAP_PER_INCOMING_DIRECTION = {
    '7': {
        (1, 0): (0, 1),
        (0, -1): (-1, 0)
    },
    '-': {
        (1, 0): (1, 0),
        (-1, 0): (-1, 0)
    },
    'F': {
        (0, -1): (1, 0),
        (-1, 0): (0, 1)
    },
    'J': {
        (0, 1): (-1, 0),
        (1, 0): (0, -1)
    },
    '|': {
        (0, -1): (0, -1),
        (0, 1): (0, 1)
    },
    'L': {
        (-1, 0): (0, -1),
        (0, 1): (1, 0)
    },
    'S': {
        (1, 0): (1, 0),
        (-1, 0): (-1, 0),
        (0, -1): (0, -1),
        (0, 1): (0, 1)
    },
}


def is_in_bounds(lines, x, y):
    return 0 <= y < len(lines) and 0 <= x < len(lines[y])


def get_map_of_links_in_loop(all_coord_links, reachability_map):
    result = defaultdict(set)
    for coord_a, coord_b in all_coord_links:
        if coord_a not in reachability_map.keys() or coord_b not in reachability_map.keys():
            continue
        result[coord_a].add(coord_b)
        result[coord_b].add(coord_a)
    return result


def find_nodes_within_loop(lines, map_of_links_in_loop):
    result = set()
    last_y_branch = None
    for y in range(len(lines)):
        in_loop = False
        for x in range(len(lines[y])):
            coord = (x, y)
            if coord not in map_of_links_in_loop:
                if in_loop:
                    result.add(coord)
                continue
            linked = map_of_links_in_loop[coord]
            up, down, left, right = (x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)
            if up in linked and down in linked:
                in_loop = not in_loop
                continue
            if left in linked and right in linked:
                continue
            y_branch = (y - 1) if up in linked else (y + 1)
            if last_y_branch is None:
                last_y_branch = y_branch
            else:
                if last_y_branch != y_branch:
                    in_loop = not in_loop
                last_y_branch = None
    return result


def find_start(grid):
    for (y, x), char in enumerate_matrix(grid):
        if char == 'S':
            return x, y
    assert False


def detect_loop(lines):
    grid = [list(l) for l in lines]
    start = find_start(grid)

    worklist = [
        (start, (-1, 0), 0),
        (start, (1, 0), 0),
        (start, (0, -1), 0),
        (start, (0, 1), 0)
    ]
    linked_coords = set()
    distance_map = {start: 0}
    while len(worklist) > 0:
        coord, (dx, dy), distance = worklist.pop()
        x, y = coord
        if not is_in_bounds(grid, x, y):
            continue
        char = grid[y][x]
        assert char != '.'
        if char != 'S' and coord in distance_map and distance_map[coord] <= distance:
            # Already reached this coord faster through another path, let's stop here
            continue
        distance_map[coord] = distance
        next_dx, next_dy = DELTA_MAP_PER_INCOMING_DIRECTION[char][(dx, dy)]
        next_x, next_y = x + next_dx, y + next_dy
        next_char = grid[next_y][next_x]
        if (next_dx, next_dy) not in DELTA_MAP_PER_INCOMING_DIRECTION[next_char]:
            # Dead end
            continue
        linked_coords.add(((x, y), (next_x, next_y)))
        linked_coords.add(((next_x, next_y), (x, y)))
        if next_char != 'S':
            worklist.append(((next_x, next_y), (next_dx, next_dy), distance + 1))
    return linked_coords, distance_map


def part1():
    lines = read_input_as_lines()
    _, distance_map = detect_loop(lines)
    return max(distance_map.values())


def part2():
    lines = read_input_as_lines()
    linked_coords, distance_map = detect_loop(lines)
    linked_in_loop_map = get_map_of_links_in_loop(linked_coords, distance_map)
    return len(find_nodes_within_loop(lines, linked_in_loop_map))


if __name__ == '__main__':
    print(part1())
    print(part2())
