from copy import copy

from puzzles.Day19.SymbolicItem import SymbolicItem


class Rule:
    def __init__(self, name, condition_map, global_rule_map, constraints_and_results):
        self.name = name
        self.condition_map = condition_map
        self.global_rule_map = global_rule_map
        self.constraints_and_results = constraints_and_results

    def get_n_satisfying_numbers(self, symbolic_item: SymbolicItem):
        result_sum = 0
        for (symbol, constraint), result in self.constraints_and_results:
            if symbol is None:
                # Always True case
                return result_sum + self.count_combinations_if_condition_is_true(result, symbolic_item)
            # Apply condition and loop
            item_with_constraint = copy(symbolic_item)
            item_with_constraint.add_true_constraint(symbol, constraint)
            result_sum += self.count_combinations_if_condition_is_true(result, item_with_constraint)
            symbolic_item = copy(symbolic_item)
            symbolic_item.add_false_constraint(symbol, constraint)
        return result_sum

    def count_combinations_if_condition_is_true(self, result, symbolic_item):
        if result == 'A':
            return symbolic_item.get_n_satisfying_numbers()
        elif result == 'R':
            return 0
        return self.global_rule_map[result].get_n_satisfying_numbers(symbolic_item)

    def apply(self, x, m, a, s):
        for cond, result in self.condition_map.items():
            if cond.evaluate(x, m, a, s):
                if result == 'A':
                    return True
                elif result == 'R':
                    return False
                return self.global_rule_map[result].apply(x, m, a, s)
