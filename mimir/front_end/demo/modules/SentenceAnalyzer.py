import re
import sys
import nltk
import json
import jieba
import codecs
import jieba.analyse
import operator
import itertools
import numpy as np
import pandas as pd
from nltk import FreqDist
from dateutil.relativedelta import relativedelta
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer
from .StringAnalyzer import *

# StringAnalyzer()
S = StringAnalyzer()

## 以句子為單位，包括切句子，提供句子內單字共現表。
class SentenceAnalyzer:
    def __init__(self):
        pass
    def sentences_splited_from_article(self, target_article):
        sentence_list = []
        sentence_clean_list = []
        for sentence in target_article.split('，'):
            sentence_list.append(sentence)
        for sp in S.sentence_punctuation_list:
            s_list = []
            for item in sentence_list:
                for n_item in item.split(sp):
                    s_list.append(n_item)
            sentence_list = s_list
        for item in sentence_list:
            sentence_clean_list.append(S.punctuation_cleaner(item))
        return sentence_clean_list

    def sentences_coshow_words_dict(self, target_batch_sentences_list): #以句子為單位
        coshow_words_dict = {}
        print('總batch句子共有{}句'.format(len(target_batch_sentences_list)))
        i = 0 
        for s in target_batch_sentences_list:
            if i % 50 == 0:
                print('目前進度第{}句'.format(i))
            for (k1,k2), v in S.string_coshow_wordspair_dict(s).items():
                if k1 != k2:
                    if (k1,k2) in list(coshow_words_dict.keys()):
                        coshow_words_dict[(k1, k2)] = coshow_words_dict.get((k1, k2)) + 1
                    elif (k2,k1) in list(coshow_words_dict.keys()):
                        coshow_words_dict[(k2, k1)] = coshow_words_dict.get((k2, k1)) + 1
                    else:
                        coshow_words_dict[(k1, k2)] = v
            i += 1
        print('Finished')
        return sorted(coshow_words_dict.items(), key=itemgetter(1), reverse=True)
