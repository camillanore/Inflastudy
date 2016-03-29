# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 20:15:31 2016

@author: NBCNO1
"""
import numpy as np
import nose.tools
from pandas.util.testing import assert_frame_equal
import pandas as pd

from inflastudy import InflaData
from inflastudy import NaivePredictions
#import InflaData
#import NaivePredictions


    
def test_naive_trajectory():
    cpi = np.random.normal(loc=2.5, size=(5,1))
    dates = ('2016-03-31','2016-06-30','2016-09-30','2016-12-31','2017-03-31')

    testdata = pd.DataFrame(cpi, index=dates)
    print(testdata)
    naive = NaivePredictions.NaivePredictions(
        testdata, prediction_horizon=4, time_convergion_quarters=3)
    print(naive.data)
    
if __name__ == '__main__':
    test_naive_trajectory()