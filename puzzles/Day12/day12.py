from functools import cache

from util import read_input_as_lines


def parse():
    for line in read_input_as_lines():
        grid, setup = line.split(' ')
        yield grid, tuple(map(int, setup.split(',')))


@cache
def hashtag_case(remaining_grid, remaining_reqs):
    next_n_broken_geysers = remaining_reqs[0]
    if '.' in remaining_grid[:next_n_broken_geysers]:
        # next req CAN'T start here - invalid
        return 0
    new_remaining_grid = remaining_grid[next_n_broken_geysers:]
    if len(new_remaining_grid) > 0:
        if new_remaining_grid[0] == '#':
            # Invalid, because there is a '#' right after it
            return 0
        if new_remaining_grid[0] == '?':
            # Must ensure separation
            new_remaining_grid = '.' + new_remaining_grid[1:]
    return count(new_remaining_grid, remaining_reqs[1:])


@cache
def question_mark_case(remaining_grid, remaining_reqs):
    result = count(remaining_grid[1:], remaining_reqs)
    next_n_broken_geysers = remaining_reqs[0]
    if ('.' not in remaining_grid[:next_n_broken_geysers]) and \
            (len(remaining_grid) <= next_n_broken_geysers or
             remaining_grid[next_n_broken_geysers] != '#'):
        # Next req could fit here, try and move onto next req
        new_grid = remaining_grid[next_n_broken_geysers:]
        if len(new_grid) > 0 and new_grid[0] == '?':
            new_grid = '.' + new_grid[1:]
        result += count(new_grid, remaining_reqs[1:])
    return result


@cache
def count(remaining_grid, remaining_reqs):
    result = 0
    if len(remaining_reqs) == 0:
        return 0 if '#' in remaining_grid else 1
    grid_length = len(remaining_grid)
    if len(remaining_grid) == 0:
        return 0

    next_n_broken_geysers = remaining_reqs[0]
    if grid_length < next_n_broken_geysers:
        return 0
    first_char = remaining_grid[0]
    if first_char == '#':
        # next req MUST start here
        result += hashtag_case(remaining_grid, remaining_reqs)
    elif first_char == '.':
        result += count(remaining_grid.lstrip('.'), remaining_reqs)
    elif first_char == '?':
        # Case: this ? is operational (is a .)
        result += question_mark_case(remaining_grid, remaining_reqs)
    else:
        assert False, repr(first_char)
    return result


@cache
def count_expanded(grid, setup, factor):
    return count('?'.join([grid] * factor), tuple(list(setup) * factor))


def part1():
    return sum(count(grid, setup) for grid, setup in parse())


def part2():
    return sum(count_expanded(grid, setup, 5) for grid, setup in parse())


if __name__ == '__main__':
    print(part1())
    print(part2())
