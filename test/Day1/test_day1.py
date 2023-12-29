import unittest

from puzzles.Day1.day1 import part1, part2
from test.TestConfig import TestConfig


class Day1Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 54605)

    def test_part2(self):
        self.assertEqual(part2(), 55429)