import os
import sys
from unittest import TestCase

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../precise_rounding')))

from precise_rounding import precise_rounding


class Test(TestCase):
    def test_precise_rounding_1(self):
        result = precise_rounding(123.45678, 0.01234)
        expected = ('123.457', '0.013')
        self.assertEqual(expected, result)

    def test_precise_rounding_2(self):
        result = precise_rounding(123.45678, 0.01008)
        expected = ('123.457', '0.010')
        self.assertEqual(expected, result)

    def test_precise_rounding_3(self):
        result = precise_rounding(123.45678, 0.515)
        expected = ('123.46', '0.52')
        self.assertEqual(expected, result)

    def test_precise_rounding_4(self):
        result = precise_rounding(123.45678, 5.123)
        expected = ('123.5', '5.2')
        self.assertEqual(expected, result)

    def test_precise_rounding_5(self):
        result = precise_rounding(123.45678, 55.123)
        expected = ('123', '56')
        self.assertEqual(expected, result)

    def test_precise_rounding_6(self):
        result = precise_rounding(453121123.456, 323451)
        expected = ('453120000', '330000')
        self.assertEqual(expected, result)

    def test_precise_rounding_7(self):
        result = precise_rounding(123.456, 0)
        expected = ('123.456', '0')
        self.assertEqual(expected, result)

    def test_precise_rounding_11(self):
        with self.assertRaises(ValueError):
            precise_rounding(1.0, -0.01)

    def test_precise_rounding_11(self):
        with self.assertRaises(ValueError):
            precise_rounding(1.0, -0.01)

    def test_precise_rounding_11(self):
        with self.assertRaises(TypeError):
            precise_rounding('abc', 0.01)

    def test_precise_rounding_12(self):
        with self.assertRaises(TypeError):
            precise_rounding(10.0, 'abc')

    def test_precise_rounding_13(self):
        with self.assertRaises(TypeError):
            precise_rounding(1.0, 0.01, 'abc')

    def test_precise_rounding_14(self):
        with self.assertRaises(ValueError):
            precise_rounding(1.0, -0.01)

    def test_precise_rounding_15(self):
        with self.assertRaises(ValueError):
            precise_rounding(1.0, 0.01, -1)
