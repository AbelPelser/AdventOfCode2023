from collections import defaultdict

from util import read_input_as_lines, remove_empty


def get_numbers_in_string(string):
    return set(map(int, remove_empty(string.split(' '))))


def parse_input_as_card_decks():
    for line in read_input_as_lines():
        card_id, numbers = line.split(': ')
        card_id = int(card_id.split(' ')[-1])
        winning, have = numbers.split(' | ')
        yield card_id, get_numbers_in_string(winning), get_numbers_in_string(have)


def part1():
    result = 0
    for _, winning, have in parse_input_as_card_decks():
        common = len(have.intersection(winning))
        if common > 0:
            result += 2 ** (common - 1)
    return result


def part2():
    n_cards = defaultdict(lambda: 1)
    for card_id, winning, have in parse_input_as_card_decks():
        our_winning_cards = have.intersection(winning)
        n_this_card = n_cards[card_id]
        for n in range(1, len(our_winning_cards) + 1):
            n_cards[card_id + n] += n_this_card
    return sum(n_cards.values())


if __name__ == '__main__':
    print(part1())
    print(part2())
