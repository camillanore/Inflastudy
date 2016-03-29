# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 21:47:15 2016

@author: Camilla Nore
"""
import numpy as np
import pandas as pd

class NaivePredictions():
    def __init__(self, actual_data, target = 2.5, col_prefix = 'PPR_dQ',
                 time_convergion_quarters = 12, prediction_horizon=16):
        """Generate Naive Predictions"""
        self.time_convergion_quarters = time_convergion_quarters
        self.target = target
        self.data = pd.DataFrame(actual_data)
        # Create the column for relative predictions, and fill with NaN.
        pred_relative_col_names = []
        # TODO(Camilla): Hvis språkbruken er "ett kvartal frem" for første
        # prediksjon i banen, bytt om til range(1, prediction_horizon+1).
        for dq in range(0, prediction_horizon):
            col_name = col_prefix + str(dq)
            pred_relative_col_names.append(col_name)
            ser = pd.Series(np.empty(len(self.data.index)), index=self.data.index)
            self.data[col_name] = ser
            #TODO(Camilla): We are now ignoring the now-casting. We have to use
            # the previous actual value to now-cast the current value.
            for i, date in enumerate(self.data.index):
                if i == 0: 
                    self.data.loc[date,col_name] = np.NaN
                    continue
                last_known = self.data.iloc[i,0]
                self.data.loc[date,col_name] = self.get_naive_value(
                    last_known, dq+1)
                                
            
    def get_naive_value(self, actual_value, delta_quarters, mode='linear'):
        """ Get one single prediction value into the future. """
        error = self.target - actual_value        
        h = error/float(self.time_convergion_quarters)
        if mode == 'linear':
            if delta_quarters > self.time_convergion_quarters:
                # If after time convergence, set to target.
                naive_forecast = self.target
            else:
                naive_forecast = actual_value + h*delta_quarters
        elif mode == 'exp':
            # This might be better for longer horizons to avoid overshoot.
            # TODO: Check this equation. Currently not in use.
            naive_forecast = actual_value + error*np.exp(-1/h*delta_quarters)
        return naive_forecast
    
    
    
def test_naive_trajectory():
    cpi = np.random.normal(loc=2.5, size=(5,1))
    dates = ('2016-03-31','2016-06-30','2016-09-30','2016-12-31','2017-03-31')

    testdata = pd.DataFrame(cpi, index=dates)
    print(testdata)
    naive = NaivePredictions(testdata, prediction_horizon=4, time_convergion_quarters=3)
    print(naive.data)
    
    
if __name__ == '__main__':
    test_naive_trajectory()