import unittest

from puzzles.Day20.day20 import part1, part2
from test.TestConfig import TestConfig


class Day20Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 818_649_769)

    def test_part2(self):
        self.assertEqual(part2(), 246_313_604_784_977)
