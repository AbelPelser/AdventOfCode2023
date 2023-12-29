import unittest

from puzzles.Day3.day3 import part1, part2
from test.TestConfig import TestConfig


class Day3Test(TestConfig, unittest.TestCase):
    def test_day3_part1(self):
        self.assertEqual(part1(), 543_867)

    def test_day3_part2(self):
        self.assertEqual(part2(), 79_613_331)
