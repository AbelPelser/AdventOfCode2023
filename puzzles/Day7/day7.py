import functools
from collections import Counter

from util import read_input_as_lines


def score_hand(hand):
    counter = Counter(hand)
    card_numbers = set(counter.values())
    if 5 in card_numbers:
        return 7
    if card_numbers == {4, 1}:
        return 6
    if card_numbers == {3, 2}:
        return 5
    if 3 in card_numbers:
        return 4
    values_list = list(counter.values())
    if values_list.count(2) == 2:
        return 3
    if 2 in card_numbers:
        return 2
    return 1


def replace_jokers(hand):
    if hand == 'JJJJJ':
        return 'AAAAA'
    most_common_card = [card for card, amount in Counter(hand).most_common() if card != 'J'][0]
    return hand.replace('J', most_common_card)


def score_hand_with_jokers(hand):
    return score_hand(replace_jokers(hand))


def compare_hands(hand_a, hand_b, scoring_function=score_hand, card_ranks='23456789TJQKA'):
    label_a, label_b = map(scoring_function, (hand_a, hand_b))
    if label_a < label_b:
        return -1
    elif label_a > label_b:
        return 1
    for card_a, card_b in zip(list(hand_a), list(hand_b)):
        index_a, index_b = map(card_ranks.index, (card_a, card_b))
        if index_a < index_b:
            return -1
        elif index_a > index_b:
            return 1
    return 0


def compare_hands_part2(hand_a, hand_b):
    return compare_hands(hand_a, hand_b, scoring_function=score_hand_with_jokers, card_ranks='J23456789TQKA')


def parse():
    hands_list = []
    bids_per_hand = {}
    for line in read_input_as_lines():
        hand, bid = line.split(' ')
        hands_list.append(hand)
        bids_per_hand[hand] = int(bid)
    return hands_list, bids_per_hand


def calculate_total_winnings(hands_list_ranked, bids_per_hand):
    return sum((i + 1) * bids_per_hand[hand] for i, hand in enumerate(hands_list_ranked))


def rank_hands_and_get_total_winnings(hands_comparator):
    hands_list, bids_per_hand = parse()
    hands_list.sort(key=functools.cmp_to_key(hands_comparator))
    return calculate_total_winnings(hands_list, bids_per_hand)


def part1():
    return rank_hands_and_get_total_winnings(compare_hands)


def part2():
    return rank_hands_and_get_total_winnings(compare_hands_part2)


if __name__ == '__main__':
    print(part1())
    print(part2())
