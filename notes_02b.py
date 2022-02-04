# How to use date and time with Pandas (2b)
# Upsampling and interpolation with .resample()
#------------------------------------------

from matplotlib.image import AxesImage
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

# Other frequencies
# B         business day frequency
# C         custom business day frequency (experimental)
# D         calendar day frequency
# W         weekly frequency
# M         month end frequency
# SM        semi-month end frequency (15th and end of month)
# BM        business month end frequency
# CBM       custom business month end frequency
# MS        month start frequency
# SMS       semi-month start frequency (1st and 15th)
# BMS       business month start frequency
# CBMS      custom business month start frequency
# Q         quarter end frequency
# BQ        business quarter endfrequency
# QS        quarter start frequency
# BQS       business quarter start frequency
# A         year end frequency
# BA, BY    business year end frequency
# AS, YS    year start frequency
# BAS, BYS  business year start frequency
# BH        business hour frequency
# H         hourly frequency
# T, min    minutely frequency
# S         secondly frequency
# L, ms     milliseconds
# U, us     microseconds
# N         nanoseconds


# asfreq and resample -----------------------------------------------------------------
print("\nasfreq and resample", "-" * 30)
# .asfreq() is a selector for the datatime values.
unrate.asfreq('M').info()
unrate.asfreq('MS').info()
unrate_r = unrate.resample('M')

u_equal = unrate.asfreq('MS').equals(unrate_r.asfreq())
print(u_equal)


#  Fill ------------------------------------------------------------------------------
print("\nFill", "-" * 30)
unrate.info()
print(unrate.head(10))

unrate_ffill = unrate.resample('D').ffill().add_suffix('_fill')
unrate_ffill.info()
print(unrate_ffill.head(10))

unrate_interp = unrate.resample('D').interpolate().add_suffix('_interp')
unrate_interp.info()
print(unrate_interp.head(10))


# Concatenating two DataFrames ------------------------------------------------------
print("\nConcatenating two DataFrames", "-" * 30)

df1 = pd.DataFrame([1, 2, 3], columns = ['df1'])
df2 = pd.DataFrame([4, 5, 6], columns = ['df2'])
df3 = pd.concat([df1, df2])
print(df3.head(10))

# axis = 1: concatenate horizontally
print('\nwith axis = 1')
df4 = pd.concat([df1, df2], axis = 1)
print(df4.head(10))

df5 = pd.concat([unrate_ffill, unrate_interp], axis = 1)
print(df5.head(10))
df5.loc['2001':'2010'].plot()
#plt.show()


# Downsampling and aggregation methods -----------------------------------------------
print("\nDownsampling and aggregation methods", "-" * 30)
nio = pd.read_csv('NIO.csv', parse_dates = ['Date'], index_col = 'Date')
nio.info()

# https://blog.csdn.net/qifeidemumu/article/details/88764211
print("\n price DataFrame")
price = pd.DataFrame(nio.Close).resample('D').asfreq().dropna()
print(type(price))
price.info()

price_mean = price.resample('M').mean()
print('\n', price_mean.head())
price_median = price.resample('M').median()
print('\n', price_median.head())

# .agg() takes a list of / a np function name. e.g. np.min np.sum
price_agg = price.resample('M').agg(['mean', 'std']).head()
print('\n', price_agg.head())

ax_p = price.plot()
monthly = price.resample('M').mean()
monthly.add_suffix('_monthly').plot(ax = ax_p)
plt.show()