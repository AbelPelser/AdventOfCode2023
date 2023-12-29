from util import read_input_as_lines

DELTA_MAP = {
    '\\': {
        (1, 0): ((0, 1),),
        (0, -1): ((-1, 0),),
        (0, 1): ((1, 0),),
        (-1, 0): ((0, -1),)
    },
    '/': {
        (1, 0): ((0, -1),),
        (0, -1): ((1, 0),),
        (0, 1): ((-1, 0),),
        (-1, 0): ((0, 1),)
    },
    '|': {
        (1, 0): ((0, 1), (0, -1),),
        (0, -1): ((0, -1),),
        (0, 1): ((0, 1),),
        (-1, 0): ((0, 1), (0, -1),)
    },
    '-': {
        (1, 0): ((1, 0),),
        (0, -1): ((1, 0), (-1, 0)),
        (0, 1): ((1, 0), (-1, 0)),
        (-1, 0): ((-1, 0),)
    },
    '.': {
        (1, 0): ((1, 0),),
        (0, -1): ((0, -1),),
        (0, 1): ((0, 1),),
        (-1, 0): ((-1, 0),)
    },
}


def parse():
    return [list(l) for l in read_input_as_lines()]


def is_in_bounds(grid, x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])


def count_energized_tiles(grid, start):
    seen = set()
    worklist = {start}
    tiles = set()
    while len(worklist) > 0:
        work_item = worklist.pop()
        if work_item in seen:
            continue
        x, y, incoming_direction = work_item
        if not is_in_bounds(grid, x, y):
            continue
        seen.add(work_item)
        tiles.add((x, y))
        tile_type = grid[y][x]
        for ndx, ndy in DELTA_MAP[tile_type][incoming_direction]:
            worklist.add((x + ndx, y + ndy, (ndx, ndy)))
    return len(tiles)


def part1():
    return count_energized_tiles(parse(), (0, 0, (1, 0)))


def part2():
    result = 0
    grid = parse()
    for y in range(len(grid)):
        result = max(count_energized_tiles(grid, (0, y, (1, 0))), result)
        result = max(count_energized_tiles(grid, (len(grid[y]) - 1, y, (-1, 0))), result)
    for x in range(len(grid[0])):
        result = max(count_energized_tiles(grid, (x, 0, (0, 1))), result)
        result = max(count_energized_tiles(grid, (x, len(grid) - 1, (0, -1))), result)
    return result


if __name__ == '__main__':
    print(part1())
    print(part2())
