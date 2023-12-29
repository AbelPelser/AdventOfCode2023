import unittest

from puzzles.Day11.day11 import part1, part2
from test.TestConfig import TestConfig


class Day11Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 9_648_398)

    def test_part2(self):
        self.assertEqual(part2(), 618_800_410_814)
