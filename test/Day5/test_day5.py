import unittest

from puzzles.Day5.day5 import part1, part2
from test.TestConfig import TestConfig


class Day5Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 251_346_198)

    def test_part2(self):
        self.assertEqual(part2(), 72_263_011)
