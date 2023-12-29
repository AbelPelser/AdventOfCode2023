import unittest

from puzzles.Day4.day4 import part1, part2
from test.TestConfig import TestConfig


class Day4Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 20829)

    def test_part2(self):
        self.assertEqual(part2(), 12_648_035)
