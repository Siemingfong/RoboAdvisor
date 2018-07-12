import os
import re
import pymongo
import datetime
import operator
import itertools
import pandas as pd
from pymongo import MongoClient
from dateutil.relativedelta import relativedelta
client = MongoClient(port=27017)

def testFunc():
    return 50

class NewsDataGet:
    def __init__(self, target_client, target_db, target_collection):
        # Link to DB's collection.
        client = MongoClient(target_client) 
        news_db = client[target_db]
        news_collection = news_db[target_collection]
        self.news_collection = news_collection
        
    def news_get_by_date(self, start_date, end_date): #ex: start_date = '2017-09-14' 
        news_collect = []
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date  = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        for item in self.news_collection.find({'Date':{'$gte': start_date, '$lte': end_date}}):
            news_collect.append(item)
            news_df = pd.DataFrame(news_collect)
        return news_df
    
    def news_get_by_cliff(self, price_tag_cliff, start_date_timedelta=-3, end_date_timedelta=3):
        news_collect = []
        news_tag_collect = []
        news_markdate_collect = [] 
        price_with_tag = price_tag_cliff[price_tag_cliff['Tag'] != 0]
        
        for index, row in price_with_tag.iterrows():
            if row['Tag'] == 1:
                news_tag = (row['Datee'].strftime('%Y%m%d'))+ 'U'
            else:
                news_tag = (row['Datee'].strftime('%Y%m%d'))+ 'D'

            #price_with_tag.set_value(index, 'Newstag', news_tag)
            start = row['Datee'] + datetime.timedelta(days=start_date_timedelta)
            end = row['Datee'] + datetime.timedelta(days=end_date_timedelta)
            today = row['Datee']

            # get news data from db
            for item in self.news_collection.find({'Date':{'$gte': start, '$lte': end}}):
                news_collect.append(item)
                news_tag_collect.append(news_tag)
                news_markdate_collect.append(today)
            # news_df: create 
            news_df = pd.DataFrame(news_collect)
            news_df['Newstag'] = news_tag_collect
            news_df['Markday'] = news_markdate_collect
            # news_df: 發生前or發生後
            news_df['BorA'] = 0
            for index, row in news_df.iterrows():
                if row['Date'] > row['Markday']:
                    news_df.set_value(index, ['BorA'], 'after')
                elif row['Date'] == row['Markday']:
                    news_df.set_value(index, ['BorA'], 'theDay')
                else:
                    news_df.set_value(index, ['BorA'], 'before')
        return news_df #news_tag_by_cliff
        
    def news_get_by_landmark(self, price_tag_landmark, start_date_timedelta=-3, end_date_timedelta=3):
        news_collect = []
        news_tag_collect = []
        news_markdate_collect = [] 
        price_with_tag = price_tag_landmark[price_tag_landmark['Tag'] != 0]
        price_history = [n*1000 for n in range(1,25)]
        i = 0
        for index, row in price_with_tag.iterrows():
            news_tag = 'Reach' + str(price_history[i]) + '!'
            price_with_tag.set_value(index, 'Newstag', news_tag)
            start = row['Datee'] + datetime.timedelta(days=start_date_timedelta)
            end = row['Datee'] + datetime.timedelta(days=end_date_timedelta)
            today = row['Datee']
            # get news data from db
            for item in self.news_collection.find({'Date':{'$gte': start, '$lte': end}}):
                news_collect.append(item)
                news_tag_collect.append(news_tag)
                news_markdate_collect.append(today)
            news_df = pd.DataFrame(news_collect)
            news_df['Markday'] = news_markdate_collect
            news_df['Newstag'] = news_tag_collect
            news_df['BorA'] = 0
            for index, row in news_df.iterrows():
                if row['Date'] > row['Markday']:
                    news_df.set_value(index, ['BorA'], 'after')
                elif row['Date'] == row['Markday']:
                    news_df.set_value(index, ['BorA'], 'theDay')
                else:
                    news_df.set_value(index, ['BorA'], 'before')
            i += 1
        return news_df #news_tag_by_landmark
