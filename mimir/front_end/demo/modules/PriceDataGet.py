import pymongo
import datetime
import pandas as pd
from pymongo import MongoClient
#from utils.mongo_tools import get_mongo_db
client = MongoClient(port=27017)

class PriceDataGet:
    def __init__(self, target_db, target_collection):
        
        # Link to DB's collection.
        price_db = MongoClient(target_client)
        price_collection = price_db[target_collection]
        
        # get price from price_collection
        price_array = []
        for n in price_collection.find():
            price_array.append(n)
            
        # from array to df
        price_df =  pd.DataFrame(price_array)        
        price_df = price_df[['Date', 'Open', 'High', 'Low', 'Close']] # re-order
        price_df['Datee'] = price_df['Date'] # make a copy col
        price_df.set_index('Date',inplace=True) # set datetime as index
        self.price_df = price_df
        
    def mark_price_cliff(self):
        # mark_method =='mm_cliff'
        price_df = self.price_df[['Open', 'High', 'Low', 'Close','Datee']]
        price_df['C_back1'] = price_df['Close'].shift(-1)  # 前一天
        price_df['C_forward1'] = price_df['Close'].shift(1) # 後一天價格
        price_df['Tag'] = 0 # 標記漲跌用 
        for index, row in price_df.iterrows():
            diff = row['C_forward1']/row['Close']
            price_df.set_value(index, 'Diff', diff)
            if diff >= 1.2:
                price_df.set_value(index, 'Tag', 1) # '大漲'
            elif diff <= 0.8:
                price_df.set_value(index, 'Tag', 2) # '大跌'
            else:
                price_df.set_value(index, 'Tag', 0) # '未標記'
        self.price_tag_cliff = price_df
        
    def mark_price_landmark(self):
        # mark_method =='mm_landmark'
        price_df = self.price_df[['Open', 'High', 'Low', 'Close','Datee']]
        price_history = [n*1000 for n in range(1,25)]
        price_df['Tag'] = 0
        k = 0
        for index, row in price_df.iterrows():
            if row['High'] > price_history[k]:
                price_df.set_value(index, 'Tag', 1) # 'history-high-tag'
                k += 1
            else:
                price_df.set_value(index, 'Tag', 0) # 'nothing'
            if k > (len(price_history)-1):
                break
        self.price_tag_landmark = price_df