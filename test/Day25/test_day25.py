import unittest

from puzzles.Day25.day25 import part1, part2
from test.TestConfig import TestConfig


class Day25Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 583_632)

    def test_part2(self):
        self.assertEqual(part2(), None)
