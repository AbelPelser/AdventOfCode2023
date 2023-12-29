from functools import cache

from util import read_input_as_lines, enumerate_matrix

DELTAS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def is_in_bounds(grid, x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])


def get_neighbours(grid, x, y):
    for dx, dy in DELTAS:
        nx, ny = x + dx, y + dy
        if is_in_bounds(grid, nx, ny):
            yield nx, ny


def parse_input():
    return [list(map(int, line)) for line in read_input_as_lines()]


def path_is_valid(path):
    return get_n_same_deltas_end(path) <= 3


@cache
def path_is_valid2(path):
    prev_delta = None
    counter = 0
    for i in range(1, len(path)):
        prev = path[i - 1]
        current = path[i]
        delta = (current[0] - prev[0], current[1] - prev[1])
        if prev_delta is None:
            counter = 1
            prev_delta = delta
            continue
        if prev_delta == delta:
            counter += 1
            if counter > 10:
                return False
        else:
            if not (4 <= counter <= 10):
                return False
            counter = 1
        prev_delta = delta
    return True


@cache
def get_n_same_deltas_end(path):
    prev_delta = None
    prev = None
    counter = 0
    for i in range(len(path) - 1, -1, -1):
        current = path[i]
        if prev is None:
            prev = current
            continue
        delta = (current[0] - prev[0], current[1] - prev[1])
        if prev_delta is None:
            prev_delta = delta
        elif prev_delta != delta:
            return counter
        counter += 1
        prev = current
    return counter


def new_try(grid, initial_node, shortest_path_per_neighbour, path_validity_function, delta_to_maintain):
    # node (tuple (x, y)) -> neighbour (tuple (x, y)) -> n_same_deltas_end -> tuple(path (list), length (int))
    worklist = {initial_node}
    for initial_nb in get_neighbours(grid, initial_node[0], initial_node[1]):
        for n_deltas_same in range(delta_to_maintain[0], delta_to_maintain[1]):
            shortest_path_per_neighbour[initial_node][initial_nb][n_deltas_same] = ([initial_node], 0)

    while len(worklist) > 0:
        current_node = worklist.pop()
        current_x, current_y = current_node
        current_node_incoming_paths_per_same_deltas_at_end = shortest_path_per_neighbour[current_node]
        for outgoing_nb_to_update in get_neighbours(grid, current_x, current_y):
            outgoing_nb_x, outgoing_nb_y = outgoing_nb_to_update
            outgoing_nb_value = grid[outgoing_nb_y][outgoing_nb_x]

            # See if there is a new shortest path from node to neighbour
            outgoing_paths_to_shorten = shortest_path_per_neighbour[outgoing_nb_to_update][current_node]
            for incoming_nb in get_neighbours(grid, current_x, current_y):
                # Skip checking paths from the neighbour we're trying to update,
                # Also skip checking paths from nodes we haven't seen before
                if incoming_nb == outgoing_nb_to_update or \
                        incoming_nb not in current_node_incoming_paths_per_same_deltas_at_end or \
                        current_node_incoming_paths_per_same_deltas_at_end[incoming_nb] is None:
                    continue
                incoming_paths_per_same_deltas_at_end = current_node_incoming_paths_per_same_deltas_at_end[incoming_nb]
                for n_same_deltas_at_end, (incoming_path, incoming_path_length) in incoming_paths_per_same_deltas_at_end.items():
                    potential_new_path = incoming_path + [outgoing_nb_to_update]
                    potential_new_path_length = outgoing_nb_value + incoming_path_length

                    new_n_same_deltas_at_end = get_n_same_deltas_end(potential_new_path)
                    if new_n_same_deltas_at_end in outgoing_paths_to_shorten:
                        _, length_to_beat = outgoing_paths_to_shorten[new_n_same_deltas_at_end]
                    else:
                        length_to_beat = 9999999999

                    if not path_validity_function(tuple(potential_new_path)):
                        continue
                    if potential_new_path_length < length_to_beat:
                        worklist.add(outgoing_nb_to_update)
                        shortest_path_per_neighbour[outgoing_nb_to_update][current_node][new_n_same_deltas_at_end] = (potential_new_path, potential_new_path_length)

    def get_shortest_path(n):
        # node (tuple (x, y)) -> neighbour (tuple (x, y)) -> n_same_deltas_end -> tuple(path (list), length (int))
        level1 = shortest_path_per_neighbour[n]
        res = None
        respath = None
        for neighbour, level2 in level1.items():
            for n_same_deltas_at_end, (path, path_length) in level2.items():
                if res is None or path_length < res:
                    res = path_length
                    respath = path
        return respath, res
    return get_shortest_path((len(grid[0]) - 1, len(grid) - 1))[1]


def get_neighbour_map(grid):
    result = {}
    for (y, x), char in enumerate_matrix(grid):
        result[(x, y)] = {(nx, ny): {} for nx, ny in get_neighbours(grid, x, y)}
    return result


def part1():
    grid = parse_input()
    return new_try(grid, (0, 0), get_neighbour_map(grid), path_is_valid, (0, 4))


def part2():
    grid = parse_input()
    return new_try(grid, (0, 0), get_neighbour_map(grid), path_is_valid2, (4, 11))


if __name__ == '__main__':
    # print(part1())
    print(part2())
