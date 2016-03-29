# -*- coding: utf-8 -*-
"""
Created on Fri Sep 04 08:16:38 2015

@author: NBCNO1
"""

import re
import numpy as np

__ppr_name_regexp = re.compile(
    (r'PPR'                  # Start with PPR
     r'(?P<quarter>\d)'      # Look for single digit quarter
     r'_'                    # seperated by an underscore
     r'(?P<year>\d\d)'       # followed by two-digit year
     r'(?P<description>.*)'  # and the description tag.
     ))

""" The regular expression for this tool. We do not want others outside to use
this regular expression. So we make it private by starting the name with __.
"""


def decode(column_name):
    """ Internal method for InflaData to get year, quarter and description
        from the column names in the input dataset.
    """
    ppr_pattern_found = __ppr_name_regexp.match(column_name)
    if not ppr_pattern_found:
        raise ValueError('Could not find ppr pattern in column name:' + column_name)
        return None
    # In the match object, the individual groups are given as a dict.
    # Ref to the regexp defined above, we will get a dictionary with:
    # {quarter=#, year=##, description='...'}
    dictionary = ppr_pattern_found.groupdict()
    return dictionary