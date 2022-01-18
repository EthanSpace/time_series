import pandas as pd

dates = pd.date_range(start = '2016', periods = 4, freq = 'Q')
data = range(1, 5)
quarterly = pd.Series(data = data, index = dates)

print(quarterly, '\n')
dates_1 = pd.date_range(start = '2016', periods = 12, freq = 'M')
print(dates_1, '\n')

quarterly.reindex(dates_1, Inplace = True)
print(quarterly, '\n')