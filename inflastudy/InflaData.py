import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

from inflastudy import decode_column_name
from inflastudy import time_tools

class InflaData(object):
    def __init__(self, filename=None, decimal_point='.'):
        if filename:
            self.load_data_file(filename, decimal_point)

    def load_data_file(self, filename, decimal_point='.'):
        """ Load raw data from csv file. """
        # self.raw_data = pd.DataFrame.from_csv(filename, sep=';')
        self.raw_data = pd.read_csv(filename, sep=';', index_col = 0, 
                                    parse_dates = True, decimal=decimal_point)
        self.cpi_predictions = self.find_data(['cpi'])
        self.cpi_jae_predictions = self.find_data(['jae','xe'], 
                                                  exclude_cols=['CPI-jae'])
        self.gap_predictions = self.find_data(['gap'], 
                                              exclude_cols=['Produksjonsgap']) 
        
    def calc_relative_data(self):    
        self.cpi_pred_relative = self.remap_to_relative_time(self.cpi_predictions, 
                                                             self.raw_data['CPI'])
        self.jae_pred_relative = self.remap_to_relative_time(self.cpi_jae_predictions, 
                                                             self.raw_data['CPI-jae'])
        self.gap_pred_relative = self.remap_to_relative_time(self.gap_predictions, 
                                                             self.raw_data['Produksjonsgap'])
        
    def find_data(self, include_cols, exclude_cols=[]):
        col_names = []
        for col_name in self.raw_data.columns:
            if any(inc in col_name for inc in include_cols):
                col_names.append(col_name)
        for ex in exclude_cols:
            if ex in col_names:
                col_names.remove(ex)
        # Pull data
        return self.raw_data.loc[:, col_names]
    
    def remap_to_relative_time(self, prediction_data, actual_data,
                               prediction_horizon=16):
        """ Convert the data to columns of how old the prediction is.
        """
        # Create a new empty DataFrame, and add the CPI column.
        index = self.raw_data.index
        slength = len(index)
        pred_relative = pd.DataFrame(index=index, data=None)
        colname_prefix = actual_data.name

        # Create the column for relative predictions, and fill with NaN.
        pred_relative_col_names = []
        # TODO(Camilla): Hvis språkbruken er "ett kvartal frem" for første
        # prediksjon i banen, bytt om til range(1, prediction_horizon+1).
        for dq in range(0, prediction_horizon):
            col_name = colname_prefix + '_dQ' + str(dq)
            pred_relative_col_names.append(col_name)
            ser = pd.Series(np.empty(slength), index=index)
            pred_relative[col_name] = ser
            pred_relative[col_name] = np.NaN
        
        # Okay now we have an empty frame. Let's fill it up...

        # Loop through all the PPR columns in CPI predictions.
        for col_name in prediction_data:
            col_info = decode_column_name.decode(col_name)
            ppr_date = time_tools.year_quarter_to_datetime(
                col_info['year'], col_info['quarter'])
            # Loop through each prediction in this PPR.
            for date in prediction_data.index:
                if date is pd.NaT:
                    continue
                prediction = prediction_data.loc[date, col_name]
                if not math.isnan(prediction):
                    # How old is the prediction, in quarters?
                    dq = time_tools.time_diff_in_quarters(ppr_date, date)
                    n_col_name = pred_relative_col_names[dq]
                    # Insert prediction, in the new dataframe.
                    pred_relative.loc[date, n_col_name] = (
                        prediction_data.loc[date, col_name])
                    #print 'Put prediction from ', col_name,
                    #      ' for ', date.strftime('%Y-%m-%d'),
                    #      ' in ', n_col_name
        return pred_relative

    def plot_relative_time_cpi_data(self):
        plt.figure('Predictions')
        
        plot_only_the_first_quarters = 6
        for i, col_name in enumerate(self.cpi_pred_relative):
            only_valid_data = np.isfinite(self.cpi_pred_relative[col_name])
            plt.plot(self.cpi_pred_relative.index[only_valid_data],
                 self.cpi_pred_relative.loc[only_valid_data,col_name],
                 '-', alpha=0.5, label=col_name)
            if i > plot_only_the_first_quarters:
                break  # Will stop the for loop.
        plt.plot(self.raw_data.index,self.raw_data.CPI,label='Actual CPI')        
        plt.legend(loc='best')
        plt.grid()