from typing import List, Dict

from puzzles.Day20.Pulse import Pulse


class Module:
    def __init__(self, name: str, targets: List[str], pulse_worklist: List[Pulse]):
        self.name = name
        self.targets: List[str] = targets
        self.state: bool = False  # False for low, True for high
        self.inputs: Dict[str, bool] = {}
        self.pulse_worklist = pulse_worklist

    def find_inputs(self, module_dict):
        for module in module_dict.values():
            if self.name in module.targets:
                self.inputs[module.name] = False

    def get_requirements_for(self, desired_status: bool):
        pass

    def receive_pulse(self, input_pulse: Pulse):
        pass

    def send_pulse(self):
        for target in self.targets:
            self.pulse_worklist.append(Pulse(self.state, target, self.name))
