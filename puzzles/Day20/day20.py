import math
from typing import Dict

from puzzles.Day20.Broadcast import Broadcast
from puzzles.Day20.Button import Button
from puzzles.Day20.Conjunction import Conjunction
from puzzles.Day20.FlipFlop import FlipFlop
from puzzles.Day20.Module import Module
from util import read_input_as_lines

BUTTON_COUNTER = 0


def parse():
    pulse_worklist = []
    modules: Dict[str, 'Module'] = {}
    rx_sender = None
    for line in read_input_as_lines():
        identifier, targets = line.split(' -> ')
        targets = targets.split(', ')
        if identifier[0] in ('%', '&'):
            module_type, module_name = identifier[0], identifier[1:]
            module_class = Conjunction if module_type == '&' else FlipFlop
        else:
            module_name = identifier
            module_class = Broadcast
        if 'rx' in targets:
            rx_sender = module_name
            assert module_class == Conjunction
        modules[module_name] = module_class(module_name, targets, pulse_worklist)

    modules['button'] = Button('button', ['broadcaster'], pulse_worklist)
    for module in modules.values():
        module.find_inputs(modules)
    return modules, pulse_worklist, rx_sender


def press_button(modules, pulse_worklist):
    assert len(pulse_worklist) == 0
    modules['button'].send_pulse()
    n_pulses_low = 0
    n_pulses_high = 0
    while len(pulse_worklist) > 0:
        next_pulse = pulse_worklist[0]
        pulse_worklist.remove(next_pulse)
        if next_pulse.pulse_type:
            n_pulses_high += 1
        else:
            n_pulses_low += 1
        target = next_pulse.target
        if target in modules:
            modules[target].receive_pulse(next_pulse)
    return n_pulses_low, n_pulses_high


def press_button2(modules, pulse_worklist, rx_sender_incoming_high_at):
    global BUTTON_COUNTER

    BUTTON_COUNTER += 1

    modules['button'].send_pulse()
    while len(pulse_worklist) > 0:
        next_pulse = pulse_worklist[0]
        pulse_worklist.remove(next_pulse)
        target = next_pulse.target
        if target == 'tj' and next_pulse.pulse_type:
            rx_sender_incoming_high_at[next_pulse.sender] = BUTTON_COUNTER
        if target in modules:
            modules[target].receive_pulse(next_pulse)


def part1():
    modules, pulse_worklist, _ = parse()
    sum_lo = sum_hi = 0
    for _ in range(1000):
        lo, hi = press_button(modules, pulse_worklist)
        sum_lo += lo
        sum_hi += hi
    return sum_lo * sum_hi


def part2():
    modules, pulse_worklist, rx_sender = parse()
    rx_sender_incoming_high_at = {m: 0 for m in modules[rx_sender].inputs.keys()}
    while not all(map(lambda button_count: button_count > 0, rx_sender_incoming_high_at.values())):
        press_button2(modules, pulse_worklist, rx_sender_incoming_high_at)
    return math.lcm(*rx_sender_incoming_high_at.values())


if __name__ == '__main__':
    print(part1())
    print(part2())
