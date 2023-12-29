import unittest

from puzzles.Day19.day19 import part1, part2
from test.TestConfig import TestConfig


class Day19Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 386_787)

    def test_part2(self):
        self.assertEqual(part2(), 131_029_523_269_531)
