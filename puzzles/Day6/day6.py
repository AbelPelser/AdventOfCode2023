from util import read_input_as_lines, mult, safe_split_to_int


def get_n_ways_to_win(t, score):
    # Quadratic equation solved using quadratic formula
    score_input = int((t - (t ** 2 - 4 * score) ** 0.5) / 2.)
    return round(abs(((t - 1) / 2.) - score_input) * 2)


def parse():
    time_line, distance_line = read_input_as_lines()
    return time_line.replace('Time:', ''), distance_line.replace('Distance:', '')


def part1():
    time_line, distance_line = parse()
    return mult(
        get_n_ways_to_win(t, score)
        for t, score in zip(safe_split_to_int(time_line), safe_split_to_int(distance_line))
    )


def part2():
    time_line, distance_line = parse()
    return get_n_ways_to_win(int(time_line.replace(' ', '')), int(distance_line.replace(' ', '')))


if __name__ == '__main__':
    print(part1())
    print(part2())
