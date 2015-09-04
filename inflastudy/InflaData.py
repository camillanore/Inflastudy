import numpy as np
import pandas as pd


class InflaData(object):
    def __init__(self, filename=None):
        if filename:
            self.load_data_file(filename)

    def load_data_file(self, filename):
        """ Load raw data from csv file. """
        self.raw_data = pd.DataFrame.from_csv(filename, sep=';')
        self.find_cpi_data()

def find_cpi_data(self):
        """ Extract the columns from raw_data that has CPI predictions.
        """
        cpi_column_names = []
        for column_name in self.raw_data.columns:
            if 'cpi' in column_name:
                cpi_column_names.append(column_name)
        self.cpi_predictions = self.raw_data.loc[:, cpi_column_names]