import unittest

from puzzles.Day14.day14 import part1, part2
from test.TestConfig import TestConfig


class Day14Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 108_918)

    def test_part2(self):
        self.assertEqual(part2(), 100_310)
