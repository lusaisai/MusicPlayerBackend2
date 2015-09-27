# coding=utf-8
import unittest
from localscan import break_string, alphanumeric_compare


class LocalScanTest(unittest.TestCase):
    def test_break_string(self):
        text = u'音乐10'
        self.assertEqual(break_string(text), [u'音', u'乐', 10], 'break string failed')

    def test_alphanumeric_compare(self):
        x = u'音乐10'
        y = u'音乐9'
        self.assertEqual(x < y, True, 'default compare failed')
        self.assertEqual(alphanumeric_compare(x, y), 1, 'alphanumeric compare failed')


if __name__ == '__main__':
    unittest.main()
