import unittest

from puzzles.Day21.day21 import part1, part2
from test.TestConfig import TestConfig


class Day21Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 3814)

    def test_part2(self):
        self.assertEqual(part2(), 632_257_949_158_206)
