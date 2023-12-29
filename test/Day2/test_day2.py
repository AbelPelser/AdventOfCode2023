import unittest

from puzzles.Day2.day2 import part1, part2
from test.TestConfig import TestConfig


class Day2Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 2156)

    def test_part2(self):
        self.assertEqual(part2(), 66909)
