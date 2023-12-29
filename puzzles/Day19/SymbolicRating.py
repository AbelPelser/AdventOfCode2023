from copy import copy

import portion
from portion import Bound


class SymbolicRating:
    def __init__(self):
        self.ranges = portion.closed(1, 4000)

    def add_constraint(self, interval):
        self.ranges = self.ranges.intersection(interval)

    def get_n_satisfying_numbers(self):
        return sum(map(self.get_n_satisfying_number_for_interval, self.ranges._intervals))

    @staticmethod
    def get_n_satisfying_number_for_interval(interval):
        lower = interval.lower
        upper = interval.upper
        if interval.right in (Bound.CLOSED, 'CLOSED'):
            upper += 1
        if interval.left in (Bound.OPEN, 'OPEN'):
            lower += 1
        return upper - lower

    def __copy__(self):
        result = SymbolicRating()
        result.ranges = copy(self.ranges)
        return result
