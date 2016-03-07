# -*- coding: utf-8 -*-
"""
Author: Camilla Nore
Date:   2015-09-04
"""
# Tools to get timedifferences in quarters

import numpy as np
import pandas as pd


def year_quarter_to_datetime(year, quarter):
    """ Convert year and quarter strings to a numpy datetime.

    This will come in handy when we want to compare times.
    We assume that year and quarter are string inputs.
    There are 3 months in each quarter. We want to return the first month
    in each quarter. E.g.:
        ('05','3') -> 2005-07
        ('11','1') -> 2011-01
    """
    quarter_int = int(quarter)           # Convert string to integer
    #TODO(Camilla): Check if Q1 should be jan or march?
    month = quarter_int*3              # Get the first month in a quarter.
    month_str = format(month, '02d')     # Convert to string, with leading 0.
    date_str = ''.join(('20', year, '-', month_str))  # E.g. '2006-07'.
    timestamp = np.datetime64(date_str)  # Convert to a numpy datetime.
    return timestamp


def time_diff_in_quarters(from_time, to_time):
    """ How many quarters is there from t1 to t2?

    This function is very strict about the input from_time and to_time. They
    have to be of the datatype np.datetime64. This is the type used by
    pandas for the timeseries index.
    """
    valid_types = (np.datetime64, pd.Timestamp)
    assert type(from_time) in valid_types, "from_time must be np.datetime64."
    assert type(to_time) in valid_types,   "to_time must be np.datetime64."
    dt = pd.Timedelta(to_time - from_time)
    days_per_quarter = (365.2425 / 4)
    d_quarter = dt.days / days_per_quarter
    return int(round(d_quarter))