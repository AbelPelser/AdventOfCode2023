from util import read_input_as_blocks, safe_split


def parse():
    blocks = list(read_input_as_blocks())

    seedline = blocks[0].split('seeds: ')[-1]
    seeds_to_plant = list(map(int, seedline.split(' ')))

    mapping_list = []
    for block in blocks[1:]:
        mapping_list.append({})
        for line in safe_split(block)[1:]:
            dst_range_start, src_range_start, range_length = map(int, line.split(' '))
            src_range = (src_range_start, src_range_start + range_length)
            dst_range = (dst_range_start, dst_range_start + range_length)
            mapping_list[-1][src_range] = dst_range
    return seeds_to_plant, mapping_list


def get_next_number(mapping_list, map_index, number):
    map_to_use = mapping_list[map_index]
    src_range_needed = None
    dst_range_needed = None
    for range_start, range_end in map_to_use.keys():
        if range_start <= number < range_end:
            src_range_needed = (range_start, range_end)
            dst_range_needed = map_to_use[src_range_needed]
            break
    if src_range_needed is None:
        return number
    offset = (number - src_range_needed[0])
    return dst_range_needed[0] + offset


def ranges_overlap(a, b):
    a_start, a_end = a
    b_start, b_end = b
    return not (a_end <= b_start or a_start >= b_end)


def get_next_number_ranges(mapping_list, map_index, input_src_range):
    map_to_use = mapping_list[map_index]
    if input_src_range[1] <= input_src_range[0]:
        return []

    map_src_range = next(filter(lambda r: ranges_overlap(input_src_range, r), map_to_use), None)
    if not map_src_range:
        return [input_src_range]
    map_dst_range = map_to_use[map_src_range]

    result_src_range_start = max(input_src_range[0], map_src_range[0])
    result_src_range_end = min(input_src_range[1], map_src_range[1])
    result_range_offset = max(0, input_src_range[0] - map_src_range[0])

    result_dst_range_start = map_dst_range[0] + result_range_offset
    result_range_length = result_src_range_end - result_src_range_start
    result_dst_range_end = result_dst_range_start + result_range_length

    result = [(result_dst_range_start, result_dst_range_end)]
    for remaining_range in [
        (map_src_range[1], input_src_range[1]),
        (input_src_range[0], map_src_range[0])
    ]:
        result += get_next_number_ranges(mapping_list, map_index, remaining_range)
    return result


def retrieve_location_of_seed(mapping_list, number):
    for i in range(len(mapping_list)):
        number = get_next_number(mapping_list, i, number)
    return number


def retrieve_location_of_seed_range(mapping_list, seed, range_length):
    ranges = [(seed, seed + range_length)]
    for map_index in range(len(mapping_list)):
        ranges_after_step = []
        for r in ranges:
            ranges_after_step += get_next_number_ranges(mapping_list, map_index, r)
        ranges = ranges_after_step
    return ranges


def part1():
    seeds_to_plant, mapping_list = parse()
    return min(map(lambda s: retrieve_location_of_seed(mapping_list, s), seeds_to_plant))


def part2():
    seeds_to_plant, mapping_list = parse()
    final_resulting_ranges = []
    for i in range(0, len(seeds_to_plant), 2):
        final_resulting_ranges += retrieve_location_of_seed_range(
            mapping_list, seeds_to_plant[i], seeds_to_plant[i + 1]
        )
    return min(final_resulting_ranges)[0]


if __name__ == '__main__':
    print(part1())
    print(part2())
