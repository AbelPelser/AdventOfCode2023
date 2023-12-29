from collections import defaultdict

import numpy as np

from util import read_input_as_lines, enumerate_matrix


def parse():
    grid_list = list(map(list, list(read_input_as_lines())))
    # Add extra layer of rocks on top
    for i in range(len(grid_list)):
        grid_list[i] = ['#'] + grid_list[i] + ['#']
    grid_list = ([['#'] * len(grid_list[0])]) + grid_list + ([['#'] * len(grid_list[0])])
    arr = np.array(grid_list)
    return arr, find_all_cubes(arr)


def find_all_cubes(arr):
    return {(x, y) for (y, x), char in enumerate_matrix(arr) if char == '#'}


def map_squares_to_cubes(arr, cubes, delta):
    result = {}
    dx, dy = delta
    height, width = arr.shape
    for x, y in cubes:
        cube_coord = (x, y)
        nx, ny = x + dx, y + dy
        while 0 <= ny < height and 0 <= nx < width and ((nx, ny) not in cubes):
            result[(nx, ny)] = cube_coord
            nx += dx
            ny += dy
    return result


def map_round_rocks_to_cubes(arr, tiles_to_cubes):
    # (cube_x, cube_y) -> {(round_x, round_y), (round_x, round_y), ...}
    result = defaultdict(set)
    for (y, x), char in enumerate_matrix(arr):
        if char == 'O':
            round_rock_coord = (x, y)
            rock_coord = tiles_to_cubes[round_rock_coord]
            result[rock_coord].add(round_rock_coord)
    return result


def create_new_grid(arr, rock_map, delta):
    new_arr = np.zeros(arr.shape, arr.dtype)
    new_arr.fill('.')
    new_arr[np.where(arr == '#')] = '#'
    dx, dy = delta
    for (cx, cy), rocks_set in rock_map.items():
        x, y = cx, cy
        for _ in range(len(rocks_set)):
            x, y = x + dx, y + dy
            new_arr[y][x] = 'O'
    return new_arr


def do_step(arr, cubes, delta):
    cube_map = map_squares_to_cubes(arr, cubes, delta)
    round_map = map_round_rocks_to_cubes(arr, cube_map)
    return create_new_grid(arr, round_map, delta)


def cycle(arr, cubes):
    for delta in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        arr = do_step(arr, cubes, delta)
    return arr


def do_cycles(arr, cubes, n_cycles):
    cache = {}
    i = 0
    while i < n_cycles:
        cache_key = str(arr.tolist())
        if cache_key in cache:
            cycle_length = i - cache[cache_key]
            n_cycles_to_jump = int((n_cycles - i) // cycle_length)
            if n_cycles_to_jump > 0:
                i += n_cycles_to_jump * cycle_length
                continue
        cache[cache_key] = i
        arr = cycle(arr, cubes)
        i += 1
    return arr


def calc_load(arr):
    height = len(arr)
    return sum(height - y - 1 for (y, _), char in enumerate_matrix(arr) if char == 'O')


def part1():
    arr, cubes = parse()
    return calc_load(do_step(arr, cubes, (0, 1)))


def part2():
    arr, cubes = parse()
    return calc_load(do_cycles(arr, cubes, 1000000000))


if __name__ == '__main__':
    print(part1())
    print(part2())
