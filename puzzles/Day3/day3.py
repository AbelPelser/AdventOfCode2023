from collections import defaultdict

from util import read_input_as_string_grid, mult

grid = read_input_as_string_grid()


def get_next_to_position(x, y):
    for dx, dy in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            yield nx, ny


def is_symbol(coord):
    x, y = coord
    return grid[y][x] not in '0123456789.'


def read_number_in_grid(grid_width, x, y):
    char = grid[y][x]
    number_str = ''
    is_included_part1 = False
    gears_next_to_number = set()
    while char.isdigit():
        number_str += char
        is_included_part1 |= any(map(is_symbol, get_next_to_position(x, y)))
        gears_next_to_digit = {(nx, ny)
                               for nx, ny in get_next_to_position(x, y)
                               if grid[ny][nx] == '*'}
        gears_next_to_number = gears_next_to_number.union(gears_next_to_digit)
        x += 1
        if x >= grid_width:
            break
        char = grid[y][x]
    return is_included_part1, number_str, x, gears_next_to_number


def part1():
    result = 0
    grid_width = len(grid[0])
    for y in range(len(grid)):
        x = 0
        while x < grid_width:
            is_included, number_str, x, _ = read_number_in_grid(grid_width, x, y)
            if is_included:
                result += int(number_str)
            x += 1
    return result


def part2():
    grid_width = len(grid[0])
    gear_map = defaultdict(list)
    for y in range(len(grid)):
        x = 0
        while x < grid_width:
            _, number_str, x, gears_next_to_number = read_number_in_grid(grid_width, x, y)
            if len(number_str) > 0:
                for gear_coord in gears_next_to_number:
                    gear_map[gear_coord].append(int(number_str))
            x += 1
    return sum(map(mult, filter(lambda l: len(l) == 2, gear_map.values())))


if __name__ == '__main__':
    print(part1())
    print(part2())
