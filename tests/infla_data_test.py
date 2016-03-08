# -*- coding: utf-8 -*-
"""
Created on Tue Sep 08 13:08:29 2015

@author: Camilla Nore
"""

# Test the InflaData class

import numpy as np
import nose.tools
from inflastudy import InflaData
from pandas.util.testing import assert_frame_equal
import pandas as pd

k_first_t_in_data = '2006-03-31'
k_test_data = 'tests/data_input.csv'
k_test_data_out = 'tests/data_expected_out.csv'


def unit_disabled(func):
    """ This is a decorator to disable a test.
        To use it, write @unit_disabled before the test.
    """
    def wrapper(func):
        func.__test__ = False
        return func
    return wrapper

def test_init():
     """ Test that creating an empty object works """
     data = InflaData.InflaData()
     assert data is not None
     
def test_init_with_data():
    """ Test loading data_file. """
    data = InflaData.InflaData(k_test_data)
    print(data)
    # Verify that the first line of data is read correctly.
    nose.tools.eq_(data.raw_data.index[0],
                   np.datetime64(k_first_t_in_data),
                   'First line date does not match')
    print('Successfully loaded test data: \n', data.raw_data)

#@unit_disabled  # This hasn't been implemented yet.
def test_cpi_data_conversion():
    """ Test converting data to relative format. """
    data = InflaData.InflaData(k_test_data)
    expected_output = pd.DataFrame.from_csv(k_test_data_out, sep=';')
    # Call to create the output data.
    data.remap_to_relative_time(prediction_horizon=5)
    print(data.raw_data.to_string(na_rep=''))
    print(expected_output.to_string(na_rep=''))
    print(data.cpi_pred_relative.to_string(na_rep=''))
    assert_frame_equal(expected_output, data.cpi_pred_relative)

