from util import read_input_as_lines, enumerate_matrix

DELTAS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def is_in_bounds(grid, x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])


def get_neighbours(grid, x, y):
    for dx, dy in DELTAS:
        nx, ny = x + dx, y + dy
        if is_in_bounds(grid, nx, ny):
            yield nx, ny


def get_neighbours_unbounded(x, y):
    for dx, dy in DELTAS:
        yield x + dx, y + dy


def get_neighbour_map_unbounded(grid):
    # Map from coordinates to neighbours if connected
    result = {}
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            l = []
            for nx, ny in get_neighbours_unbounded(x, y):
                dx = dy = 0
                nx_real, ny_real = nx % len(grid[0]), ny % len(grid)
                if grid[ny_real][nx_real] == '#':
                    continue
                if nx < 0:
                    dx = -1
                elif nx_real != nx:
                    dx = 1
                elif ny < 0:
                    dy = -1
                elif ny_real != ny:
                    dy = 1
                l.append(((nx_real, ny_real), (dx, dy)))
            result[(x, y)] = set(l)
    return result


def get_neighbour_map(grid):
    # Map from coordinates to neighbours if connected
    result = {}
    for (y, x), _ in enumerate_matrix(grid):
        result[(x, y)] = {(nx, ny) for nx, ny in get_neighbours(grid, x, y)
                          if grid[ny][nx] != '#'}
    return result


def parse_grid():
    return list(map(list, read_input_as_lines()))


def find_start(grid):
    for (y, x), char in enumerate_matrix(grid):
        if char == 'S':
            return x, y
    assert False


def find_next_number(list_of_ints):
    if all(map(lambda i: i == 0, list_of_ints[3:])):
        return 0
    differences = []
    for i in range(1, len(list_of_ints)):
        differences.append(list_of_ints[i] - list_of_ints[i - 1])
    return list_of_ints[-1] + find_next_number(differences)


def new_attempt(grid, n_steps):
    width = len(grid[0])
    offset = n_steps % (2 * width)  # 65
    target_steps = offset + 10 * width
    reachable_per_step = find_reachable_spots_part2(target_steps)

    index = target_steps
    related_list = []
    while index > 0:
        related_list.append(reachable_per_step[index])
        index -= 2 * width
    related_list.reverse()
    steps_iter = target_steps
    while steps_iter <= n_steps:
        n = find_next_number(related_list)
        steps_iter += 2 * width
        related_list = related_list[-15:]
        related_list.append(n)
    return related_list[-2]


def find_reachable_spots_part1(n_steps):
    grid = parse_grid()
    neighbour_map = get_neighbour_map(grid)
    result_n = 0
    seen = set()
    reachable_this_step = {find_start(grid)}

    for i in range(n_steps):
        if i % 2 == 0:
            result_n += len(reachable_this_step)
        reachable_next_step = set()
        next_seen = set()
        while len(reachable_this_step) > 0:
            x, y = reachable_this_step.pop()
            next_seen.add((x, y))
            reachable_next_step = reachable_next_step.union(neighbour_map[(x, y)].difference(seen))
        reachable_this_step = reachable_next_step
        seen = next_seen
    result_n += len(reachable_this_step)
    return result_n


def find_reachable_spots_part2(n_steps):
    grid = parse_grid()
    neighbour_map = get_neighbour_map_unbounded(grid)
    reachable_even = 0
    reachable_odd = 0
    seen = set()
    reachable_this_step = {(find_start(grid), (0, 0))}
    results_per_step = {}

    for i in range(n_steps):
        if i % 2 == 0:
            reachable_even += len(reachable_this_step)
            results_per_step[i] = reachable_even
        else:
            reachable_odd += len(reachable_this_step)
            results_per_step[i] = reachable_odd
        reachable_next_step = set()
        next_seen = set()
        while len(reachable_this_step) > 0:
            (x, y), (gx, gy) = reachable_this_step.pop()
            next_seen.add(((x, y), (gx, gy)))
            for (nx, ny), (dgx, dgy) in neighbour_map[(x, y)]:
                ngx, ngy = gx + dgx, gy + dgy
                if ((nx, ny), (ngx, ngy)) in seen:
                    continue
                reachable_next_step.add(((nx, ny), (ngx, ngy)))
        reachable_this_step = reachable_next_step
        seen = next_seen
    if n_steps % 2 == 0:
        reachable_even += len(reachable_this_step)
        results_per_step[n_steps] = reachable_even
    else:
        reachable_odd += len(reachable_this_step)
        results_per_step[n_steps] = reachable_odd
    return results_per_step


def part1():
    return find_reachable_spots_part1(64)


def part2():
    return new_attempt(parse_grid(), 26_501_365)


if __name__ == '__main__':
    print(part1())
    print(part2())
