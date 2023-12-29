import unittest

from puzzles.Day9.day9 import part1, part2
from test.TestConfig import TestConfig


class Day9Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 1_995_001_648)

    def test_part2(self):
        self.assertEqual(part2(), 988)
