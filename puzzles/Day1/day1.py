from util import safe_split, read_input


def get_sum_of_calibration_values(string):
    result = 0
    for line in safe_split(string):
        for c in list(line):
            if c.isdigit():
                a = c
                break
        for c in list(line)[::-1]:
            if c.isdigit():
                b = c
                break
        result += int(a + b)
    return result


def part1():
    return get_sum_of_calibration_values(read_input())


def part2():
    text = read_input()
    text = (text.replace('one', 'o1e')
            .replace('two', 't2o')
            .replace('three', 't3e')
            .replace('four', '4')
            .replace('five', '5e')
            .replace('six', '6')
            .replace('seven', '7n')
            .replace('eight', 'e8t')
            .replace('nine', 'n9e'))
    return get_sum_of_calibration_values(text)


if __name__ == '__main__':
    print(part1())
    print(part2())
