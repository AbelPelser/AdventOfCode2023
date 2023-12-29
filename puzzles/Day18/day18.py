from util import read_input_as_lines

DELTAS = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, -1),
    'D': (0, 1)
}

HEXCODE_DELTA_MAP = {
    0: 'R',
    1: 'D',
    2: 'L',
    3: 'U'
}


def parse(use_hexcodes=False):
    for line in read_input_as_lines():
        delta, distance, hexcode = line.split(' ')
        if not use_hexcodes:
            distance = int(distance)
        else:
            # Remove braces
            hexcode = hexcode[1:-1]
            delta = HEXCODE_DELTA_MAP[int(hexcode[-1])]
            distance = int(hexcode[1:-1], base=16)
        yield distance, DELTAS[delta]


def part1():
    x, y = 0, 0
    surface_sum = 0
    border_length = 0
    for distance, (dx, dy) in parse():
        border_length += distance
        nx, ny = x + distance * dx, y + distance * dy
        surface_sum += x * ny - nx * y
        x, y = nx, ny
    return round(surface_sum * 0.5 + border_length * 0.5 + 1)


def part2():
    x, y = 0, 0
    surface_sum = 0
    border_length = 0
    for distance, (dx, dy) in parse(use_hexcodes=True):
        border_length += distance
        nx, ny = x + distance * dx, y + distance * dy
        surface_sum += x * ny - nx * y
        x, y = nx, ny
    return round(surface_sum * 0.5 + border_length * 0.5 + 1)


if __name__ == '__main__':
    print(part1())
    print(part2())
