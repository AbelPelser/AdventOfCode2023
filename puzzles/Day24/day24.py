import z3

from util import read_input_as_lines


def parse():
    data = []
    for line in read_input_as_lines():
        p, v = line.split(' @ ')
        px, py, pz = map(int, p.split(', '))
        vx, vy, vz = map(int, v.split(', '))
        data.append(((px, py, pz), (vx, vy, vz)))
    return data


def check_if_lines_cross(position_a, speed_a, position_b, speed_b):
    px_a, py_a = position_a
    vx_a, vy_a = speed_a
    px_b, py_b = position_b
    vx_b, vy_b = speed_b
    slope_a = vy_a / vx_a
    slope_b = vy_b / vx_b
    if slope_a == slope_b:
        return None
    cross_y_axis_a = py_a - slope_a * px_a
    cross_y_axis_b = py_b - slope_b * px_b
    cross_x = (cross_y_axis_a - cross_y_axis_b) / (slope_b - slope_a)
    cross_y = cross_y_axis_a + slope_a * cross_x
    in_the_past_a = (vx_a > 0 and cross_x < px_a) or (
            vx_a < 0 and cross_x > px_a)
    in_the_past_b = (vx_b > 0 and cross_x < px_b) or (
            vx_b < 0 and cross_x > px_b)
    if in_the_past_a or in_the_past_b:
        return None
    return cross_x, cross_y


def part1(lower_bound=200000000000000, upper_bound=400000000000000):
    d = parse()
    count = 0
    for i, ((px_a, py_a, _), (vx_a, vy_a, _)) in enumerate(d):
        for (px_b, py_b, _), (vx_b, vy_b, _) in d[i + 1:]:
            cross_at = check_if_lines_cross((px_a, py_a), (vx_a, vy_a),
                                            (px_b, py_b), (vx_b, vy_b))
            if cross_at is None:
                continue
            cross_x, cross_y = cross_at
            if lower_bound <= cross_x <= upper_bound and lower_bound <= cross_y <= upper_bound:
                count += 1
    return count


def part2():
    data = parse()[:3]  # Only need 3 lines
    s = z3.Solver()
    aL = z3.Int('aL')
    bL = z3.Int('bL')
    cL = z3.Int('cL')
    xL0 = z3.Int('xL0')
    yL0 = z3.Int('yL0')
    zL0 = z3.Int('zL0')

    def create_constraints(i, position, speed):
        px, py, pz = position
        vx, vy, vz = speed
        C = z3.Int(f'C{i}')
        s.add((xL0 + (aL * C)) == (px + (vx * C)))
        s.add((yL0 + (bL * C)) == (py + (vy * C)))
        s.add((zL0 + (cL * C)) == (pz + (vz * C)))

    for i, (position, speed) in enumerate(data):
        create_constraints(i, position, speed)
    res = s.check()
    if str(res) == 'sat':
        m = s.model()
        return int(str(m[xL0])) + int(str(m[yL0])) + int(str(m[zL0]))
    assert False


if __name__ == '__main__':
    print(part1())
    print(part2())
