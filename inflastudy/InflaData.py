import numpy as np
import pandas as pd


class InflaData(object):
    def __init__(self, filename=None):
        if filename:
            self.loadDataFile(filename)

    def loadDataFile(self, filename):
        self.raw_data = pd.DataFrame.from_csv(filename, sep=';')
