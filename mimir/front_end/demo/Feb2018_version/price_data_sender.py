## Code Info
# Version: 2018-03-10
# Data info: daily OHLC Bitcoin (USD) Price
# Data source: download from https://www.coindesk.com/price/

## Init the data to DB for the first time

import json
import pymongo
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from pymongo import MongoClient


# Read data
csv_path = './coindesk-bpi-USD-ohlc_data-2013-01-01_2018-07-02.csv'

# coindesk-bpi-USD-ohlc_data-2013-01-01_2018-07-02

df = pd.read_csv(csv_path)

# Remove last 2 rows which isnt required
# df = df.drop(df.index[[-1,-2]])


# Modify date format to datetime
for index, row in df.iterrows():
    x = datetime.datetime.strptime(row['Date'], '%Y/%m/%d %H:%M')
    df.set_value(index, 'Date', x)

# Send to DB
_list = []
for index, row in df.iterrows():
    temp = {
        "Date": row['Date'],
        "Open": row['Open'],
        "High": row['High'],
        "Low": row['Low'],
        "Close": row['Close']
    }
    _list.append(temp)
    
# import urllib.parse
# username = urllib.parse.quote_plus('root')
# password = urllib.parse.quote_plus('')
# client = MongoClient('mongodb://%s:%s@140.112.145.148:26666' % (username, password))
# db = client.BTC_PRICE_DB

client = MongoClient('mongodb://localhost:27017/')
db = client.mimir
for _ in _list:
    db.BTC_COINDESK_DAILY_PRICE_COLLECTION.insert_one(_)
print('Database Updated')