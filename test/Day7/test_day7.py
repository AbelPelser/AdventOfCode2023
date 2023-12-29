import unittest

from puzzles.Day7.day7 import part1, part2
from test.TestConfig import TestConfig


class Day7Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 249_726_565)

    def test_part2(self):
        self.assertEqual(part2(), 251_135_960)
