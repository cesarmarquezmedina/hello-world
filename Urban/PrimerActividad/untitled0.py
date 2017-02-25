import pandas as pd
import pandas_datareader.data as web #conda install -c anaconda pandas-datareader=0.2.1
import numpy as np
import matplotlib.pyplot as plt
import sklearn
import pylab as pl
from sklearn.linear_model import LinearRegression

google = web.DataReader('GOOG', data_source = 'google', start = '3/14/2009', end = '4/14/2016')
google = google.drop('Volume', axis = 1 )
google['Ticks'] = range(0,len(google.index.values))

plt.scatter()