# -*- coding: utf-8 -*-

from .context import deezer

import unittest


class TestSuite(unittest.TestCase):
    """Test cases for Deezer logs analytics."""

    def test_checking_good_file(self):
        self.assertTrue(deezer.check_file('listen-20150521.log'))
        
    def test_checking_bad_file(self):
        self.assertFalse(deezer.check_file('20150521.log'))
        self.assertFalse(deezer.check_file('wrong-20150521.log'))
        self.assertFalse(deezer.check_file('listen-0150521.log'))
        self.assertFalse(deezer.check_file('listen-20150521.csv'))


if __name__ == '__main__':
    unittest.main()
