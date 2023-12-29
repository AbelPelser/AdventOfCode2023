import portion

from puzzles.Day19.Condition import TRUE_COND, Condition
from puzzles.Day19.Rule import Rule
from puzzles.Day19.SymbolicItem import SymbolicItem
from util import read_input_as_blocks, safe_split


def equation_to_interval(equation_str):
    number = int(equation_str[1:])
    if equation_str[0] == '<':
        return portion.closed(1, number - 1)
    return portion.closed(number + 1, 4000)


def parse_rules(lines):
    result = {}
    for line in lines:
        name = line.split('{')[0]
        content = line.split('{')[1].split('}')[0]
        conditions_map = {}
        constraints_and_results = []
        for subrule in content.split(','):
            if ':' not in subrule:
                cond = TRUE_COND
                target_rule = subrule
                constraint = None
                symbol = None
            else:
                cond_str, target_rule = subrule.split(':')
                symbol = cond_str[0]
                cond = Condition(cond_str)
                constraint = equation_to_interval(cond_str[1:])
            constraints_and_results.append(((symbol, constraint), target_rule))
            conditions_map[cond] = target_rule
        result[name] = Rule(name, conditions_map, result, constraints_and_results)
    return result


def parse_items(lines):
    result = []
    for line in lines:
        x = int(line.split('x=')[1].split(',')[0])
        m = int(line.split('m=')[1].split(',')[0])
        a = int(line.split('a=')[1].split(',')[0])
        s = int(line.split('s=')[1].split('}')[0])
        result.append((x, m, a, s))
    return result


def parse():
    rule_str, item_str = read_input_as_blocks()
    return parse_items(safe_split(item_str)), parse_rules(safe_split(rule_str))


def part1():
    items, rules = parse()
    return sum(map(sum, ((x, m, a, s) for (x, m, a, s) in items if rules['in'].apply(x, m, a, s))))


def part2():
    items, rules = parse()
    return rules['in'].get_n_satisfying_numbers(SymbolicItem())


if __name__ == '__main__':
    print(part1())
    print(part2())
