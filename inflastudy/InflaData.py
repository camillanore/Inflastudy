import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

from inflastudy import decode_column_name
from inflastudy import time_tools

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
    
    def remap_to_relative_time(self, prediction_horizon=16):
        """ Convert the data to columns of how old the prediction is.
        """
        # Create a new empty DataFrame, and add the CPI column.
        cpi_ser = self.raw_data.CPI
        index = self.raw_data.index
        slength = len(index)
        self.cpi_pred_relative = pd.DataFrame(index=index, data=cpi_ser)

        # Create the column for relative predictions, and fill with NaN.
        cpi_pred_relative_col_names = []
        # TODO(Camilla): Hvis språkbruken er "ett kvartal frem" for første
        # prediksjon i banen, bytt om til range(1, prediction_horizon+1).
        for dq in range(0, prediction_horizon):
            col_name = 'PPR_dQ' + str(dq)
            cpi_pred_relative_col_names.append(col_name)
            ser = pd.Series(np.empty(slength), index=index)
            self.cpi_pred_relative[col_name] = ser
            self.cpi_pred_relative[col_name] = np.NaN
        
        # Okay now we have an empty frame. Let's fill it up...

        # Loop through all the PPR columns in CPI predictions.
        for col_name in self.cpi_predictions:
            col_info = decode_column_name.decode(col_name)
            ppr_date = time_tools.year_quarter_to_datetime(
                col_info['year'], col_info['quarter'])
            # Loop through each prediction in this PPR.
            for date in self.cpi_predictions.index:
                prediction = self.cpi_predictions.loc[date, col_name]
                if not math.isnan(prediction):
                    # How old is the prediction, in quarters?
                    dq = time_tools.time_diff_in_quarters(ppr_date, date)
                    n_col_name = cpi_pred_relative_col_names[dq]
                    # Insert prediction, in the new dataframe.
                    self.cpi_pred_relative.loc[date, n_col_name] = (
                        self.cpi_predictions.loc[date, col_name])
                    #print 'Put prediction from ', col_name,
                    #      ' for ', date.strftime('%Y-%m-%d'),
                    #      ' in ', n_col_name

    def plot_relative_time_cpi_data(self):
        plt.figure('Predictions')
        plt.plot(self.raw_data.index,self.raw_data.CPI,label='Actual CPI')
        plot_only_the_first_quarters = 6
        for i, col_name in enumerate(self.cpi_pred_relative):
            only_valid_data = np.isfinite(self.cpi_pred_relative[col_name])
            plt.plot(self.cpi_pred_relative.index[only_valid_data],
                 self.cpi_pred_relative.loc[only_valid_data,col_name],
                 '-x', label=col_name)
            if i > plot_only_the_first_quarters:
                break  # Will stop the for loop.
                
        plt.legend()
        plt.grid()