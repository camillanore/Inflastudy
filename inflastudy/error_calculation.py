# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 21:35:06 2016

@author: NBCNO1
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PredictionError():
    def __init__(self, prediction_relative, actual_data):
        """ Create the prediction error object based on two data series:
            prediction_relative containing the dq columns
            actual_data containing the data to compare with as the first col.
            
            prediction = actual + prediction_error
        """
        # Empty dataframe for error
        self.pred_error = pd.DataFrame(index=prediction_relative.index)
        
        # Loop the cpi predictions
        for i, col_name in enumerate(prediction_relative.columns):
            err_name = col_name + '_err'
            self.pred_error[err_name] = (
                prediction_relative[col_name] - actual_data)
        
        self._error_statistics()
                
    def _error_statistics(self):
        # Find the mean, squaremean and std of the error.
        self.pred_error_sqmean = self.pred_error.apply(np.square).apply(np.mean)
        self.pred_error_mean = self.pred_error.apply(np.mean)
        self.pred_error_rmse = np.sqrt(self.pred_error_sqmean)
        self.pred_error_std = self.pred_error.apply(np.std)
        self.horizon_range = range(1,len(self.pred_error_sqmean.index)+1)
        #print('pred error std', self.pred_error_std)
    
    def plot_selected(self, selected_quarters = [2,4,8,12], only_selected=True):
        selected_colnames = ['dQ'+str(q) for q in selected_quarters]
        plt.figure()
        for i, col_name in enumerate(self.pred_error):
            only_valid_data = np.isfinite(self.pred_error[col_name])
            if any(q in col_name for q in selected_colnames):
                style = '-'
                label = col_name
            elif not only_selected:
                style = '--'
                label = None
            else:
                continue
            plt.plot(self.pred_error.index[only_valid_data],
                     self.pred_error.loc[only_valid_data,col_name],
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
