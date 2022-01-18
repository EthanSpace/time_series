# How to use date and time with Pandas (1)
#------------------------------------------

import pandas as pd
from datetime import datetime 
import numpy as np
import matplotlib.pyplot as plt

# Timestamp -------------------------
print("Timestamp", "-" * 20)
# Create a time point.
time_stamp = pd.Timestamp(datetime(2022, 1, 1))
ts2 = pd.Timestamp('2022-01-01')
ts3 = pd.Timestamp('2022-01-01 00:00:00')

print(time_stamp.year)
print(ts2.year)
print(ts3.year)

print(time_stamp.weekday())
print(time_stamp.dayofweek)
# weekday() returns the day of the week represented by the date. Monday == 0 … Sunday == 6
print(time_stamp.day_name())
# day_name returns the name of the day

#Attributes:
#   .second .minute .hour .day .month .quarter .year .weekofyear .dayofweek .dayofyear


# Period -----------------------------
print("Period", "-" * 20)
# Create a time constructor with staring date on Jan 31st 2022 and frequency of 1 month.
# The default period starts on the last day
period = pd.Period('2022-01')

print("month ", period.month)
print("day ", period.day)
print("hour ", period.hour)

print("next month ", (period + 1).month)

period_2 = pd.Period('2022-01', 'D')
period_3 = pd.Period('2022-01', 'M')
print("freq: D, day ", period_2.day)
print("freq: M, day ", period_3.day)

ts4 = period_2.to_timestamp()
time_stamp_3 = pd.Timestamp('2022-01-01')
period_4 = time_stamp_3.to_period('D')
print("month ", period_4.month)
print("day ", period_4.day)
print("freq ", period_4.freq)

period_5 = pd.Period(2022, freq = 'A-Jan')


# Date_range --------------------------
print("Period", "-" * 20)
# Create a list of timestamps with a constant frequency
time_index_1 = pd.date_range(start = '2022-1-1', periods = 12, freq = 'M')
time_index_2 = pd.date_range(start = '2022-1-1', periods = 12, freq = 'D')
print(time_index_1)
print(time_index_2)
print(time_index_1[2])
print(time_index_1.to_period())

#Create a time series
df_1 = pd.DataFrame({'data': time_index_1})
data = np.random.random(size = 12)
df_2 = pd.DataFrame(data = data, index = time_index_1)
print(df_2)
#DataFrame view table: 
#   set break >> Run and Debug >> Variables >> (right click) >> view

#Frequency aliases and time info
#   (H)our, (D)ay, (W)eek, (M)onth, (Q)uarter, Year (A)


# Conversion --------------------------------
print("Conversion", "-" * 20)

nio = pd.read_csv('NIO.csv')
nio.info()

#change data format 
nio.Date = pd.to_datetime(nio.Date)
# pd column names can be refered to directly with dot
nio.info()

#Set a column as index .set_index()
nio.set_index('Date', inplace = True)
nio.info()

'''
#Print a picture
nio.Close.plot(title = 'NIO Stock Price')
plt.tight_layout()
plt.show()

#If a dataframe contains multiple column, and if all needed to be ploted against index
nio.plot(subplots = True)
plt.tight_layout()
plt.show()
'''
# Slicing and selecting --------------------------
print("Slicing", "-" * 20)

# Quary for all dates in the month/ year
# FutureWarning: Indexing a DataFrame with a datetimelike index using a single string to slice the rows, like `frame[string]`, is deprecated and will be removed in a future version. 
# Use `frame.loc[string]` instead.
# nio_spet = nio.loc['2021-9']
nio_sept = nio['2021-9']
nio_sept.info()
# Slicing includes last month
nio_4th_quar = nio['2021-9' : '2021-12']
nio_4th_quar.info()
# Exact lookup
nio_spet = nio.loc['2021-9']
# print(nio_sept)
nio_2021_0601_Close = nio.loc['2021-6-1', 'Close']
print(nio_2021_0601_Close)

# Set Frequency -----------------------------
print("\nSet Frequency", "-" * 30)

# .asfreq('D') convert DataTimeIndex to calendar day frequency
#   other frequency abbrs are also good for this
#freq 'B' - Business day
nio.info()
nio.asfreq('M').info()

#Upsampling - changing to a higher frequency, may cause NaN value due to missing data
#   One way to deal with it
#   Selecting the NaN values by -- nio[nio.Close.isnull()]


# Tool1: Stock Price Comparision ---------------------------------
print("\nTool1", "-" * 30)
#   Compare the stock price for NIO in the last quarter by month
prices = pd.DataFrame()
for month in ['2021-9', '2021-10', '2021-11', '2021-12']:
    # In this way, price_per_month is a Pandas Series
    price_per_month = nio.loc[month, 'Close'].reset_index(drop = True)
    # In this way, price_per_month is a Pandas DataFrame
    #price_per_month = nio.loc[month, ['Close']].reset_index(drop = True)

    price_per_month.rename(month, inplace = True)
    # Only Dataframe uses this context -- 
    # price_per_month.rename(columns = {'Close' : month}, inplace = True)

    prices = pd.concat([prices, price_per_month], axis = 1)

prices.info()
print(prices.head()) 
prices.plot(title = 'NIO Stock Price Comparison in 4th Quarter')
# plt.show()


# Tool2: Stock Price Loading --------------------------------
print("\nTool2", "-" * 30)
# Reading CSV with pd.read_csv() It can do the parsing along loading
nio_2 = pd.read_csv('NIO.csv', parse_dates = ['Date'], index_col = 'Date')
nio_2.info()
print(nio_2.head())
nio_2['Shifted'] = nio_2.Close.shift() # default period = 1
nio_2['Lagged'] = nio_2.Close.shift(-1) # lagged can take negative number
print(nio_2.head())
nio_2['Change'] = nio_2.Close.div(nio_2.Shifted) - 1
print(nio_2.head()) 
# .div() for divide and .sub() for subtract and .mul() for multiply
# .pct_change() .pct_change(30) is the percent change of the value n period ago