from util import read_input_as_lines


def cmp(a, b):
    if b > a:
        return 1
    if b < a:
        return -1
    return 0


def get_all_cubes_of_brick(f, t):
    (fx, fy, fz), (tx, ty, tz) = f, t
    dx, dy, dz = cmp(fx, tx), cmp(fy, ty), cmp(fz, tz)
    while (fx, fy, fz) != (tx, ty, tz):
        yield fx, fy, fz
        fx, fy, fz = fx + dx, fy + dy, fz + dz
    yield fx, fy, fz


def fall(brick_data):
    new_all_cubes = set()
    new_brick_data = set()
    brick_data = sorted(brick_data, key=lambda t: max(t[0][2], t[1][2]))
    for (fx, fy, fz), (tx, ty, tz) in brick_data:
        while fz > 1 and tz > 1 and not any(
                map(lambda c: c in new_all_cubes, get_all_cubes_of_brick((fx, fy, fz - 1), (tx, ty, tz - 1)))):
            fz -= 1
            tz -= 1
        f, t = (fx, fy, fz), (tx, ty, tz)
        new_brick_data.add((f, t))
        new_all_cubes = new_all_cubes.union(set(get_all_cubes_of_brick(f, t)))
    return new_brick_data, new_all_cubes


def fall2(brick_data):
    new_all_cubes = set()
    new_brick_data = set()
    brick_data = sorted(brick_data, key=lambda t: max(t[0][2], t[1][2]))
    res = 0
    for (fx, fy, fz), (tx, ty, tz) in brick_data:
        ofz, otz = fz, tz
        while fz > 1 and tz > 1 and not any(
                map(lambda c: c in new_all_cubes, get_all_cubes_of_brick((fx, fy, fz - 1), (tx, ty, tz - 1)))):
            fz -= 1
            tz -= 1
        if not (ofz == fz and otz == tz):
            res += 1
        f, t = (fx, fy, fz), (tx, ty, tz)
        new_brick_data.add((f, t))
        new_all_cubes = new_all_cubes.union(set(get_all_cubes_of_brick(f, t)))
    return res


def brick_can_be_downed(brick, brick_data, all_cubes):
    brick_data = brick_data.copy()
    all_cubes = all_cubes.copy()
    brick_data.remove(brick)
    f, t = brick
    all_cubes = all_cubes.difference(set(get_all_cubes_of_brick(f, t)))
    test_brick_data, test_all_cubes = fall(brick_data)
    return test_brick_data == brick_data and test_all_cubes == all_cubes


def get_n_chain_reaction(brick, brick_data):
    brick_data = brick_data.copy()
    brick_data.remove(brick)
    return fall2(brick_data)


def parse():
    brick_positions = set()
    for line in read_input_as_lines():
        f, t = line.split('~')
        fx, fy, fz = map(int, f.split(','))
        tx, ty, tz = map(int, t.split(','))
        brick_positions.add(((fx, fy, fz), (tx, ty, tz)))
    fallen_data, fallen_cubes = fall(brick_positions)
    return fallen_data, fallen_cubes


def part1():
    result = 0
    fallen_data, fallen_cubes = parse()
    for brick in fallen_data:
        if brick_can_be_downed(brick, fallen_data, fallen_cubes):
            result += 1
    return result


def part2():
    result = 0
    fallen_data, fallen_cubes = parse()
    for brick in fallen_data:
        result += get_n_chain_reaction(brick, fallen_data)
    return result


if __name__ == '__main__':
    print(part1())
    print(part2())
