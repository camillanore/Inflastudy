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
        self.find_cpi_jae_data()

    def find_cpi_data(self):
        """ Extract the columns from raw_data that has CPI predictions.
        """
        cpi_column_names = []
        for column_name in self.raw_data.columns:
            if 'cpi' in column_name:
                cpi_column_names.append(column_name)
        self.cpi_predictions = self.raw_data.loc[:, cpi_column_names]
    
    def find_cpi_jae_data(self):
        """ Extract the columns from raw_data that has CPI-jae.
        Normally the columns are labeled with 'jae', e.g.: PPR1_05jae. In the
        period from PPR2_08 to PPR2_13, (2008 - 2013), the reported values were
        'xe'. The background for this change is described here [1]:
        http://www.norges-bank.no/Statistikk/Inflasjon/Indikatorer-for-prisvekst/Endret-beregningsmetode-for-KPIXE/
        """
        jae_column_names = []
        for column_name in self.raw_data.columns:
            if ('xe' in column_name) or ('jae' in column_name):
                jae_column_names.append(column_name)
        # The real CPI-jae column is also detected. We remove this to only be
        # left with the predictions.
        if 'CPI-jae' in jae_column_names:
            jae_column_names.remove('CPI-jae')
        self.cpi_jae_predictions = self.raw_data.loc[:, jae_column_names]