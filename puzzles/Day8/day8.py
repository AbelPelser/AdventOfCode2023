from math import lcm

from util import read_input_as_blocks, safe_split


def parse():
    sequence, nodes = read_input_as_blocks()
    sequence = [c for c in sequence if c in ('R', 'L')]

    left_map = {}
    right_map = {}
    all_nodes = set()
    for node_line in safe_split(nodes):
        frm, to = node_line.split(' = (')
        all_nodes.add(frm)
        left, right = to.split(', ')
        left_map[frm] = left
        right_map[frm] = right[:-1]
    return sequence, all_nodes, {'R': right_map, 'L': left_map}


# Assumption: Every -A node always only ends up in a single -Z node
# Assumption: When -Z node is visited at step x, the next time that node will be visited will be at step 2x
# (i.e. cycles perfectly predictably)
def find_cycles(sequence, left_right_mapping, node):
    seen = set()
    counter = index = 0
    t = (node, counter)
    while True:
        seen.add(t)
        node = left_right_mapping[sequence[index]][node]
        counter += 1
        index = counter % len(sequence)
        t = (node, index)
        if node.endswith('Z'):
            return counter


def part1():
    sequence, all_nodes, left_right_mapping = parse()
    current = 'AAA'
    counter = 0
    while current != 'ZZZ':
        direction = sequence[counter % len(sequence)]
        current = left_right_mapping[direction][current]
        counter += 1
    return counter


def part2():
    sequence, all_nodes, left_right_mapping = parse()
    start_nodes = {n for n in all_nodes if n.endswith('A')}
    z_cycles = [find_cycles(sequence, left_right_mapping, node) for node in start_nodes]
    return lcm(*z_cycles)


if __name__ == '__main__':
    print(part1())
    print(part2())
