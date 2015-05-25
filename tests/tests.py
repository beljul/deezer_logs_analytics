# -*- coding: utf-8 -*-

from .context import deezer

import unittest
import os
import shutil

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
        dir = '/tmp/deezer_test_logs'
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        f = open(dir + "/listen-00000000.log", "w")
        f.write("1|1|FR|1|1\n");
        f.write("1|1|FR|1|1\n");
        f.write("2|2|FR|2|2\n");
        f.write("2|1|FR|2|2\n");
        f.write("3|1|FR|2|2\n");
        f.close()

        deezer.parse(dir)
        res = '/tmp/deezer_test_logs/results_00000000/'
        # Two providers == two results files created
        self.assertTrue(os.path.exists(res + 'report_1.csv'))
        self.assertTrue(os.path.exists(res + 'report_2.csv'))
        
        f1 = open(res + 'report_1.csv')
        # Check information for the first one
        # Two listening
        line1 = f1.readlines()[0].split(';')
        self.assertTrue(int(line1[3]) == 2)
        # But only one user
        self.assertTrue(int(line1[4]) == 1)
        # 100% of market share
        self.assertTrue(float(line1[5]) == 1.0)
        f1.close()
        
        f2 = open(res + 'report_2.csv')
        # Check information for the second one
        lines = f2.readlines()
        line1 = lines[0].split(';')
        # Two listening for song 2
        self.assertTrue(int(line1[3]) == 2)
        # With two different users
        self.assertTrue(int(line1[4]) == 2)
        # 66% of market share
        self.assertTrue(float(line1[5]) == 0.666666666667)
        
        line2 = lines[1].split(';')
        # Only one listening for song 3
        self.assertTrue(int(line2[3]) == 1)
        # So only one user too
        self.assertTrue(int(line2[4]) == 1)
        # 33% of market share
        self.assertTrue(float(line2[5]) == 0.333333333333)
        f2.close()
        
        shutil.rmtree(dir)
        
if __name__ == '__main__':
    unittest.main()
