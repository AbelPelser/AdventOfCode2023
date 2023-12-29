from puzzles.Day20.Module import Module
from puzzles.Day20.Pulse import Pulse


class Broadcast(Module):
    def receive_pulse(self, input_pulse: Pulse):
        self.send_pulse()
