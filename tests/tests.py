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

    def test_checking_good_line(self):
        self.assertTrue(deezer.check_line('25321423|4225664|FR|199|42'))

    def test_checking_bad_content_line(self):
        self.assertFalse(deezer.check_line('asong|4225664|FR|199|42'))
        self.assertFalse(deezer.check_line('25321423|user|FR|199|42'))
        self.assertFalse(deezer.check_line('25321423|4225664|FRR|199|42'))
        self.assertFalse(deezer.check_line('25321423|4225664|fr|199|42'))
        self.assertFalse(deezer.check_line('25321423|4225664|99|199|42'))
        self.assertFalse(deezer.check_line('25321423|4225664|FR|provider|42'))
        self.assertFalse(deezer.check_line('25321423|4225664|FR|199|offer'))

    def test_checking_bad_format_line(self):
        self.assertFalse(deezer.check_line('25321423;4225664|FR|199|42'))
        self.assertFalse(deezer.check_line('|25321423|4225664|FR|199|42'))
        self.assertFalse(deezer.check_line('25321423|4225664|FR|199|42&'))

    def test_parse(self):
        deezer.parse('/home/beljul/Projects/logs')
if __name__ == '__main__':
    unittest.main()
