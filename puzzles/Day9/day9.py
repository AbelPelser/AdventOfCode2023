from util import read_input_as_lines, safe_split_to_int


def find_next_number(list_of_ints):
    if all(map(lambda i: i == 0, list_of_ints)):
        return 0
    differences = []
    for i in range(1, len(list_of_ints)):
        differences.append(list_of_ints[i] - list_of_ints[i - 1])
    return list_of_ints[-1] + find_next_number(differences)


def parse():
    return map(safe_split_to_int, read_input_as_lines())


def part1():
    return sum(map(find_next_number, parse()))


def part2():
    return sum(map(find_next_number, map(lambda l: list(reversed(l)), parse())))


if __name__ == '__main__':
    print(part1())
    print(part2())
