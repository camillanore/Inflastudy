# -*- coding: utf-8 -*-
"""
Created on Tue Sep 08 13:08:29 2015

@author: Camilla Nore
"""

# Test the InflaData class

import numpy as np
import nose.tools
from inflastudy import InflaData

k_first_t_in_data = '2006-03-31'
k_test_data = 'tests/test_data_input.csv'

def test_init():
     """ Test that creating an empty object works """
     data = InflaData.InflaData()
     assert data is not None
     
def test_init_with_data():
    """ Test loading data_file. """
    data = InflaData.InflaData(k_test_data)
    print data
    # Verify that the first line of data is read correctly.
    nose.tools.eq_(data.raw_data.index[0],
                   np.datetime64(k_first_t_in_data),
                   'First line date does not match')
    print 'Successfully loaded test data: \n', data.raw_data
