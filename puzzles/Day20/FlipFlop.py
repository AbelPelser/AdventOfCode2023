from puzzles.Day20.Module import Module
from puzzles.Day20.Pulse import Pulse


class FlipFlop(Module):
    def receive_pulse(self, input_pulse: Pulse):
        if input_pulse.pulse_type:
            return
        self.state = not self.state
        self.send_pulse()
