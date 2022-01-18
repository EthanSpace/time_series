# How to use date and time with Pandas (2)
#------------------------------------------

import pandas as pd
from datetime import datetime 
import numpy as np
import matplotlib.pyplot as plt

# Comparing Stock Performance ------------------------------
print('\nComparing Stock Performance', '-' * 30)
nio = pd.read_csv('NIO.csv', parse_dates = ['Date'], index_col = 'Date')
print(nio.head())

first_Close = nio.Close.iloc[0]
print('.iloc[0]: ', first_Close)

first_Close = nio.loc['2021-01-04', 'Close']
print(".loc['2021-01-04', 'Close']: ", first_Close)

first_Close = nio.Close.loc['2021-01-04']
print(".loc['2021-01-04']: ", first_Close)

normalized = nio.Close.div(first_Close).mul(100)
normalized.plot(title = 'NIO Normalized Close Price')
#plt.show()
#plt.cla()

nio.info()
normalized = nio.div(nio.iloc[0])
normalized.plot(subplots = True)
#plt.show()
#plt.cla()

# Comparing Stock Performance ------------------------------
print('\nComparing with a benchmark', '-' * 30)
benchmark = pd.read_csv('S&P500.csv', parse_dates = ['Date'], index_col = 'Date')
benchmark.info()
print(benchmark.head())

renamed_benchmark = pd.DataFrame(index = nio.index)
renamed_benchmark.info()

for header in benchmark.columns:
    # Compare to notes_01.py line 141-151. [Index have to match.]
    selected_col = benchmark[header]
    selected_col.rename('nio' + header, inplace = True)
    # Convert Pandas Dataframe to Float with commas and negative numbers
    selected_col = pd.DataFrame(pd.to_numeric(selected_col.str.replace(',', ''), errors = 'coerce', downcast = 'float'), index = nio.index)
    #renamed_benchmark = renamed_benchmark.join(selected_col)
    renamed_benchmark = pd.concat([renamed_benchmark, selected_col], axis = 1)
'''
for header in benchmark.columns:
    # Compare to notes_01.py line 141-151. Index have to match
    selected_col = benchmark[header].reset_index(drop = True)
    selected_col.rename('nio' + header, inplace = True)
    # Convert Pandas Dataframe to Float with commas and negative numbers
    selected_col = pd.DataFrame(pd.to_numeric(selected_col.str.replace(',', ''), errors = 'coerce', downcast = 'float'))
    selected_col.index = benchmark.index
    print("\nhead\n")
    print(selected_col.head())
    selected_col.info()
    print("\nnext\n")
    #renamed_benchmark = renamed_benchmark.join(selected_col)
    renamed_benchmark = pd.concat([renamed_benchmark, selected_col], axis = 1)
    renamed_benchmark.info()
renamed_benchmark.info()
print(renamed_benchmark.head())
'''

nio = pd.concat([nio, renamed_benchmark], axis = 1 )
print(nio.head())
normalized = nio.div(nio.iloc[0]).mul(100) - 100
print(normalized.head())
normalized[['Close', 'nioClose']].plot()
diff = normalized['nioClose'].sub(normalized['Close'], axis = 0)
# .sub(..., axis = 0) means to subtract a series from each DataFram column by aligning indexes

# WHY is it plotted on the preivous graph?
# Only DataFrame is ploted on a different graph. Series are ploted to the nearest open graph by default.
pd.DataFrame(diff).plot(title = "Different between S&P500")
#plt.show()


# Changing the frequency: resampling ------------------------------------
print('\nResampling', '-' * 30)

dates = pd.date_range(start = '2016', periods = 4, freq = 'Q')
data = range(1, 5)
quarterly = pd.Series(data = data, index = dates)
print(quarterly, '\n')

monthly = quarterly.asfreq('M')
print(monthly, '\n')

monthly = monthly.to_frame('baseline')
print(monthly, '\n')

# Upsampling: bfill - backfill, ffill - forward fill
monthly['ffill'] = quarterly.asfreq('M', method = 'ffill')
monthly['bfill'] = quarterly.asfreq('M', method = 'bfill')
monthly['value'] = quarterly.asfreq('M', fill_value = 0)
print(monthly, '\n')

# Add missing months: .reindex()
dates = pd.date_range(start = '2016', periods = 12, freq = 'M')
print(dates, '\n')
new_quarterly = quarterly.reindex(dates)
print(new_quarterly, '\n')  