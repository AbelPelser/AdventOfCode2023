from collections import defaultdict

from util import read_input


def get_hash(string):
    current = 0
    for c in list(string):
        current += ord(c)
        current *= 17
        current %= 256
    return current


def part1():
    return sum(map(get_hash, read_input().split(',')))


def part2():
    boxes = defaultdict(dict)
    for seq in read_input().split(','):
        label = seq.split('=')[0].split('-')[0]
        box_dict = boxes[get_hash(label)]
        if '-' in seq and label in box_dict:
            del box_dict[label]
        elif '=' in seq:
            focal_length = int(seq.split('=')[-1])
            box_dict[label] = focal_length
    result = 0
    for box_n, box_dict in boxes.items():
        for lens_n, (_, focal_length) in enumerate(box_dict.items()):
            result += (box_n + 1) * (lens_n + 1) * focal_length
    return result


if __name__ == '__main__':
    print(part1())
    print(part2())
