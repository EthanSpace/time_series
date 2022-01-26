# How to use date and time with Pandas (2b)
# Upsampling and interpolation with .resample()
#------------------------------------------

import pandas as pd
from datetime import datetime 
import numpy as np
import matplotlib.pyplot as plt

# Frequency conversion and transformation methods -------------------------------------
unrate_raw = pd.read_csv('unemployment_rate.csv')

# to_datetime() 
# Source link: https://www.dataindependent.com/pandas/pandas-to-datetime/
# to_datetime(your_date_data, format = "your_formattings")
# Formatting code: 
# E.g. 
# s = pd.Series(['My 3date is 01199002', 'My 3date is 02199015')
# s = pd.to_datetime(s, format="My 3date is %m%Y%d")

unrate_raw['Month'] = pd.to_datetime(unrate_raw['Month'], format = "%b-%y")
unrate_raw.set_index('Month', inplace = True)
unrate_raw.info()
print(unrate_raw.head())

print("\nunrate", "-" * 30)
unrate = pd.DataFrame(unrate_raw['Total'])
# Without DataFrame conversion, unrate_raw['Total'] is a series
unrate.info()
print(unrate.head())

# Resampling frequency and alias
# calendar month end       M        2017-04-30
# calendar month start     MS       2017-04-01
# Business month end       BM       2017-04-28
# Business month start     BMS      2017-04-03


print("\nasfreq and resample", "-" * 30)
# .asfreq() is a selector for the datatime values.
unrate.asfreq('M').info()
unrate.asfreq('MS').info()
unrate_r = unrate.resample('M')

u_equal = unrate.asfreq('MS').equals(unrate_r.asfreq())
print(u_equal)

