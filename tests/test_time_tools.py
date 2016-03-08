# -*- coding: utf-8 -*-
"""
Author: Camilla Nore
Date:   2015-09-04
"""
# Test the time tools 

import nose.tools
import numpy as np
from inflastudy import time_tools


def test_year_quarter_to_datetime():
    """ Test year and quarter to datetime: """
    #             Date       Year   Q 
    test_data = [['2005-03-31', '05', '1'],
                 ['2011-12-31', '11', '4'],
                 ['2015-09-30', '15', '3']]
    for [date_str, year, quarter] in test_data:
        from_time_tools = time_tools.year_quarter_to_datetime(year, quarter)
        expected = np.datetime64(date_str)
        nose.tools.eq_(from_time_tools, expected,
                       'Wrong datetime detected: %s -> %s'%(
                           str(from_time_tools), str(expected)))


def test_time_diff_in_quarters():
    """ Test convert time difference to nearest quarters: """
    test_data = [['2005-01', '2005-04', 1],
                 ['2015-01-01', '2015-08-07', 2],
                 ['2015-01-01', '2015-07-07', 2],   # Check that it rounds up.
                 ['2015-12-31', '2015-01-01', -4],  # Check negative.
                 ]
    for [from_time_str, to_time_str, d_quarter] in test_data:
        t1 = np.datetime64(from_time_str)
        t2 = np.datetime64(to_time_str)
        dt = time_tools.time_diff_in_quarters(t1, t2)
        nose.tools.eq_(dt, d_quarter, ''.join((
                       'Error in delta quarter result, expected:',
                       str(d_quarter), 'return was:', str(dt))))