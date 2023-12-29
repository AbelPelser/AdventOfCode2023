from util import read_input_as_lines, mult

LIMITS_PART1 = {
    'green': 13,
    'red': 12,
    'blue': 14
}


def game_is_possible(colors):
    for subset in colors.split('; '):
        for color in subset.split(', '):
            nr, ctype = color.split(' ')
            nr = int(nr)
            if nr > LIMITS_PART1[ctype]:
                return False
    return True


def get_power_of_game(colors):
    needed = {'red': 0, 'green': 0, 'blue': 0}
    for subset in colors.split('; '):
        for color in subset.split(', '):
            nr, ctype = color.split(' ')
            nr = int(nr)
            if nr > needed[ctype]:
                needed[ctype] = nr
    return mult(needed.values())


def part1():
    result = 0
    for line in read_input_as_lines():
        gid, colors = line.split(': ')
        gid = gid.split(' ')[-1]
        if game_is_possible(colors):
            result += int(gid)
    return result


def part2():
    return sum(get_power_of_game(line.split(': ')[1]) for line in read_input_as_lines())


if __name__ == '__main__':
    print(part1())
    print(part2())
