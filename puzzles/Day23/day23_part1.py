from functools import cache

from util import read_input_as_lines


DELTAS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ARROW_DELTAS = {
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, 1),
    '^': (0, -1)
}


@cache
def is_in_bounds(grid, x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])


@cache
def get_neighbours(grid, x, y):
    result = set()
    for dx, dy in DELTAS:
        nx, ny = x + dx, y + dy
        if is_in_bounds(grid, nx, ny):
            result.add((nx, ny))
    return result


def arrow_helper(grid, arrow_x, arrow_y, coords_seen):
    coordinates_seen_during_arrow_path = {(arrow_x, arrow_y)}
    c = grid[arrow_y][arrow_x]
    assert c in ARROW_DELTAS
    while c in ARROW_DELTAS:
        dx, dy = ARROW_DELTAS[c]
        (arrow_x, arrow_y) = (arrow_x + dx, arrow_y + dy)
        assert (arrow_x, arrow_y) not in coordinates_seen_during_arrow_path
        if (arrow_x, arrow_y) in coords_seen:
            return None
        coordinates_seen_during_arrow_path.add((arrow_x, arrow_y))
        c = grid[arrow_y][arrow_x]
        assert c != '#'
    return coordinates_seen_during_arrow_path, (arrow_x, arrow_y)


def find_possible_hikes_part1(grid, start, goal):
    # length, seen, position
    worklist = [(1, {start}, start)]
    result = []
    while len(worklist) > 0:
        current_length, current_seen, (x, y) = worklist.pop()
        for nx, ny in get_neighbours(grid, x, y):
            if (nx, ny) == goal:
                result.append(current_seen.union({(nx, ny)}))
                continue
            if (nx, ny) in current_seen:
                continue
            match grid[ny][nx]:
                case '#':
                    continue
                case '.':
                    new_seen = current_seen.union({(nx, ny)})
                    worklist.append((current_length + 1, new_seen, (nx, ny)))
                case arrow:
                    arrow_res = arrow_helper(grid, nx, ny, current_seen)
                    if arrow_res is None:
                        continue
                    seen_from_arrow, (nx, ny) = arrow_res
                    new_seen = current_seen.union(seen_from_arrow)
                    worklist.append((current_length + len(seen_from_arrow), new_seen, (nx, ny)))
    return result


def part1():
    lines = read_input_as_lines()
    grid = list(map(list, lines))
    grid = tuple(tuple(l) for l in grid)
    paths = find_possible_hikes_part1(grid, (1, 0), (len(grid[-1]) - 2, len(grid) - 1))
    best_path = None
    best_len = None
    for r in paths:
        if best_path is None or len(r) > best_len:
            best_path = r
            best_len = len(r)
    return best_len - 1


if __name__ == '__main__':
    print(part1())
