import numpy as np

from util import read_input_as_blocks, safe_split, enumerate_matrix


def read_as_arrays():
    arrays = []
    for block in read_input_as_blocks():
        arrays.append(np.array(list(map(list, safe_split(block)))))
    return arrays


def check_horizontal(arr, ignore=None):
    arr_len = len(arr)
    for i in range(1, arr_len):
        if ignore == i:
            continue
        space_to_mirror = min(i, arr_len - i)
        above = np.flip(arr[i - space_to_mirror:i], axis=0)
        below = arr[i:i + space_to_mirror, :]
        if (above == below).all():
            return i
    return -1


def check_vertical(arr, ignore=None):
    arr_len = len(arr[0])
    for i in range(1, arr_len):
        if ignore == i:
            continue
        space_to_mirror = min(i, arr_len - i)
        left = arr[:, i - space_to_mirror:i]
        right = arr[:, i:i + space_to_mirror]
        if (np.flip(left, axis=1) == right).all():
            return i
    return -1


def valid_result(v, h):
    return (v == -1) != (h == -1)


def calculate_score(v, h):
    return v if v != -1 else 100 * h


def find_smudge_score(arr):
    v_orig, h_orig = check_vertical(arr), check_horizontal(arr)
    for (y, x), char in enumerate_matrix(arr):
        old = char
        arr[y, x] = '#' if old == '.' else '.'
        v, h = check_vertical(arr, ignore=v_orig), check_horizontal(arr, ignore=h_orig)
        arr[y, x] = old
        if v != -1 and v != v_orig:
            return v
        if h != -1 and h != h_orig:
            return h * 100


def find_clean_mirror_score(arr):
    return calculate_score(check_vertical(arr), check_horizontal(arr))


def part1():
    return sum(map(find_clean_mirror_score, read_as_arrays()))


def part2():
    return sum(map(find_smudge_score, read_as_arrays()))


if __name__ == '__main__':
    print(part1())
    print(part2())
