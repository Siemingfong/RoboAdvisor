# Import Modules
import sys
import nltk
import json
import jieba
import codecs
import jieba.analyse
import requests
import datetime
import operator
import itertools
import pandas as pd
from nltk import FreqDist
from dateutil.relativedelta import relativedelta
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer

class TFIDFX:
    def __init__(self):
        pass
    
    def stpwdstxt_to_list(self, stop_words_txt_path):
        stpwds_list = []
        with open(stop_words_txt_path, 'r', encoding = 'utf-8-sig') as f:
            for line in f:
                stpwds_list.append(S.punctuation_cleaner(line))
        return stpwds_list
    
    def string_to_seg_words_string(self, target_string):
        return ' '.join(S.string_cutter(target_string)[0])
    
    def tfidf_func(self, target_dict, min_idf_show, max_idf_show):
        tfidf_dict = {}
        mix_list = []
        for item in list(target_dict.values()):
            mix_list.append(item)

        # set stop_word_list
        stop_word_list = self.stpwdstxt_to_list('./bitcoin_news_stop_words.txt')
        vectorizer = TfidfVectorizer(min_df=1, stop_words = stop_word_list)
        print('start fit_transform the data')
        tfidf = vectorizer.fit_transform(mix_list)
        words = vectorizer.get_feature_names()

        for i in range(len(mix_list)):
            print('----Document {0}----'.format(list(target_dict.keys())[i]))
            tfidf_dict[list(target_dict.keys())[i]] = []
            for j in range(len(words)):
                if tfidf[i, j] > min_idf_show and tfidf[i, j] < max_idf_show:
                    tfidf_dict[list(target_dict.keys())[i]].append((words[j], tfidf[i,j]))
        return tfidf_dict
    
    def check_tfidf_dict_total_words(self, target_tfidf_dict):
        total_words = []
        for key in list(target_tfidf_dict.keys()):
            for (x, y) in target_tfidf_dict[key]:
                total_words.append(x)
        total_words = list(set(total_words))
        return total_words # node_list

    def check_tfidf_dict_co_show(self, target_tfidf_dict):
        coshow_words_dict = {}
        total_words = []
        for v in target_tfidf_dict.values():
            word_list = []
            for (x, y) in v:
                word_list.append(x)
            words_pair = self.list_coshow_wordspair_dict(word_list)
            total_words += word_list
            for (k1, k2) in words_pair:
                if k1 != k2:
                    if (k1,k2) in list(coshow_words_dict.keys()):
                        coshow_words_dict[(k1, k2)] = coshow_words_dict.get((k1, k2)) + 1
                    elif (k2,k1) in list(coshow_words_dict.keys()):
                        coshow_words_dict[(k2, k1)] = coshow_words_dict.get((k2, k1)) + 1
                    else:
                        coshow_words_dict[(k1, k2)] = 1
        return list(set(total_words)), sorted(FreqDist(coshow_words_dict).items(), key = operator.itemgetter(1), reverse=True)

    def list_coshow_wordspair_dict(self, target_list):
        wordspair_dict = {}
        for item in list(itertools.combinations(set(target_list), 2)):
            wordspair_dict[item] = 1
        return wordspair_dict