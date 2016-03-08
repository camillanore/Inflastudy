# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 21:35:06 2016

@author: NBCNO1
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PredictionError():
    def __init__(self, prediction_relative, col_name_actual='CPI'):
        # Empty dataframe for error
        self.cpi_pred_error = pd.DataFrame(index=prediction_relative.index)
        
        # Loop the cpi predictions
        for i, col_name in enumerate(prediction_relative.columns):
            if 'CPI' in col_name:  # Skip the CPI column
                continue
            err_name = col_name + '_err'
            self.cpi_pred_error[err_name] = (
                - prediction_relative[col_name] + prediction_relative.CPI)
        
        self._error_statistics()
                
    def _error_statistics(self):
        # Find the mean, squaremean and std of the error.
        self.pred_error_sqmean = self.cpi_pred_error.apply(np.square).apply(np.mean)
        self.pred_error_mean = self.cpi_pred_error.apply(np.mean)
        self.pred_error_rmse = np.sqrt(self.pred_error_sqmean)
        self.pred_error_std = self.cpi_pred_error.apply(np.std)
        self.horizon_range = range(1,len(self.pred_error_sqmean.index)+1)
        print('pred error std', self.pred_error_std)
    
    def plot_selected(self, 
                      selected_columns = ['PPR_dQ2_err', 'PPR_dQ4_err', 
                                          'PPR_dQ8_err', 'PPR_dQ12_err',]):
        plt.figure()        
        selected_columns = ['PPR_dQ2_err', 'PPR_dQ4_err', 'PPR_dQ8_err', 'PPR_dQ12_err',]
        for i, col_name in enumerate(self.cpi_pred_error):
            only_valid_data = np.isfinite(self.cpi_pred_error[col_name])
            if col_name in selected_columns:
                style = '-'
                label = col_name
            else:
                style = '--'
                label = None
                continue #If we want to completely skip these.
            plt.plot(self.cpi_pred_error.index[only_valid_data],
                 self.cpi_pred_error.loc[only_valid_data,col_name],
                 style, label=label)
        plt.title('Error data')
        plt.grid()
        plt.legend()
        
    def plot_rms(self):        
        plt.figure()
        plt.title('Root of mean square error')
        plt.errorbar(self.horizon_range,           # The x-axis
                     self.pred_error_rmse[:],   # The line
                     yerr=self.pred_error_std)     # The error bars
        plt.xlabel('Prediction horizon in quarters')
        plt.grid()
    
    def plot_mean(self):
        plt.figure()
        plt.title('Mean of error')
        plt.errorbar(self.horizon_range,           # The x-axis
                     self.pred_error_mean[:],   # The line
                     yerr=self.pred_error_std)     # The error bars
        plt.xlabel('Prediction horizon in quarters')
        plt.grid()
