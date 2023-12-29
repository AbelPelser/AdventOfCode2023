from copy import copy

from puzzles.Day19.SymbolicRating import SymbolicRating
from util import mult


class SymbolicItem:
    def __init__(self):
        self.constraints = {rating: SymbolicRating() for rating in ('x', 'm', 'a', 's')}

    def add_true_constraint(self, symbol, constraint):
        self.constraints[symbol].add_constraint(constraint)

    def add_false_constraint(self, symbol, constraint):
        self.add_true_constraint(symbol, constraint.complement())

    def get_n_satisfying_numbers(self):
        return mult(map(SymbolicRating.get_n_satisfying_numbers, self.constraints.values()))

    def __copy__(self):
        result = SymbolicItem()
        result.constraints = {key: copy(value) for key, value in self.constraints.items()}
        return result
