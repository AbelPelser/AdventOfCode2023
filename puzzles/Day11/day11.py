import numpy as np

from util import read_input_as_array


def sum_distances_with_expansion(grid, factor):
    galaxies = np.argwhere(grid == '#').tolist()
    empty_cols = np.where(np.all(grid == '.', axis=0))[0].tolist()
    empty_rows = np.where(np.all(grid == '.', axis=1))[0].tolist()

    n_galaxies = len(galaxies)
    result = 0
    # Basic sum
    for i in range(n_galaxies):
        y_from, x_from = galaxies[i]
        for y_to, x_to in galaxies[i:]:
            result += abs(y_to - y_from) + abs(x_to - x_from)

    # Expansion
    for col in empty_cols:
        n_left = len([(y, x) for y, x in galaxies if x < col])
        n_right = n_galaxies - n_left
        result += n_left * n_right * (factor - 1)

    for row in empty_rows:
        n_above = len([(y, x) for y, x in galaxies if y < row])
        n_below = n_galaxies - n_above
        result += n_above * n_below * (factor - 1)
    return result


def part1():
    return sum_distances_with_expansion(read_input_as_array(), 2)


def part2():
    return sum_distances_with_expansion(read_input_as_array(), 1_000_000)


if __name__ == '__main__':
    print(part1())
    print(part2())
