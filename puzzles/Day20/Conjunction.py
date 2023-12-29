from puzzles.Day20.Module import Module
from puzzles.Day20.Pulse import Pulse


class Conjunction(Module):
    def receive_pulse(self, input_pulse: Pulse):
        self.inputs[input_pulse.sender] = input_pulse.pulse_type
        self.state = not all(self.inputs.values())
        self.send_pulse()

    def get_requirements_for(self, desired_status: bool):
        pass
