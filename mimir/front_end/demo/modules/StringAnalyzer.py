import re
import sys
import nltk
import json
import jieba
import jieba.analyse
import requests
import datetime
import operator
import itertools
import pandas as pd
from nltk import FreqDist
from dateutil.relativedelta import relativedelta

# Text Dictionary
jieba.set_dictionary('./front_end/demo/modules/dict.txt') # 繁體字詞庫   
jieba.load_userdict("./front_end/demo/modules/bitcoin.txt") # 自訂字詞庫
jieba.analyse.set_stop_words('./front_end/demo/modules/bitcoin_news_stop_words.txt')
from operator import itemgetter

class StringAnalyzer:
    def __init__(self):
        self.punctuation_mark_list = ['[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`，。{|}~「」＜＞〈〉《》【】（）？：、！+*＊“”]', '\n', '\xa0', ' ', '\u3000', '\u200b', '\t']
        self.sentence_punctuation_list = ['，,。？?！!']
    def string_cutter(self, target_string, high_freq_choice = 1, show_count_limit = 5, word_text_count = 2):
        target_string = self.punctuation_cleaner(target_string)
        # 0.seg_word_list: 總斷詞列表
        seg_word_list = []
        seg_words = jieba.cut(target_string, cut_all=False)
        for word in seg_words:
            seg_word_list.append(word)
            
        # 1.words_used_count: 資訊
        words_used_count = [('total_words:', len(seg_word_list)), ('used_words:', len(set(seg_word_list)))]
        
        # 2 sorted_seg_word_fdist: 以次數由高至低排列列表。
        sorted_seg_word_fdist = sorted(FreqDist(seg_word_list).items(), key = operator.itemgetter(1), reverse=True)
        
        # 3 content_high_freq_words_tuple: 高次數詞使用列表+次數。
        high_freq_words_tuple = []
        high_freq_words = []
        if high_freq_choice == 1:         # 3.1 以次數>show_count，字組字數>word_text_count，為選擇
            for item_tuple in sorted_seg_word_fdist:
                if item_tuple[1] >= show_count_limit and len(item_tuple[0]) >= word_text_count:
                    high_freq_words_tuple.append(item_tuple)
        elif high_freq_choice == 2:     # 3.2 以次數前10名，字組字數>word_text_count，為選擇
            temp_list = []
            for item_tuple in sorted_seg_word_fdist:
                if len(item_tuple[0]) >= word_text_count:
                    temp_list.append(item_tuple)                
            high_freq_words_tuple = temp_list[:10]
            
        # 4 high_freq_words: 高次數詞列表。
        for item in high_freq_words_tuple:
            high_freq_words.append(item[0])
        return seg_word_list, words_used_count, sorted_seg_word_fdist, high_freq_words_tuple, high_freq_words  
    
    def string_to_ngram(self, target_string):
        target_string = self.punctuation_cleaner(target_string)
        text_list = self.string_to_text_list(target_string)
        bigram_list = self.text_list_to_bigram(text_list)
        bigram_freqdict_sorted = self.ngram_freqdict_sorted(self.bigram_list_to_freqdict(bigram_list))
        bigram_freqdict_result = self.ngram_high_freq_result(bigram_freqdict_sorted)
        trigram_list = self.text_list_to_trigram(text_list)
        trigram_freqdict_sorted = self.ngram_freqdict_sorted(self.trigram_list_to_freqdict(trigram_list))
        trigram_freqdict_result = self.ngram_high_freq_result(trigram_freqdict_sorted)
        return bigram_freqdict_result, trigram_freqdict_result

    def string_coshow_wordspair_dict(self, target_string):
        word_list = self.string_cutter(target_string=target_string, high_freq_choice=1, show_count_limit=1,word_text_count=2)[4]
        wordspair_dict = {}
        for item in list(itertools.combinations(set(word_list), 2)):
            wordspair_dict[item] = 1
        return wordspair_dict
    
    def punctuation_cleaner(self, target_string):
        for item in self.punctuation_mark_list:
            target_string = re.sub(item,'', target_string)
        return target_string  
    
    def string_to_text_list(self, target_string):
        text_list=[text for text in target_string]
        return text_list
    
    def text_list_to_bigram(self, text_list):
        return [text_list[i:i+2] for i in range(0,len(text_list)-1)]
    
    def text_list_to_trigram(self, text_list):
        return [text_list[i:i+3] for i in range(0,len(text_list)-2)]
    
    def bigram_list_to_freqdict(self, bigram_list):
        bigramfreqdict=dict()
        for (ch1,ch2) in bigram_list:
            bigramfreqdict[(ch1, ch2)]=bigramfreqdict.get((ch1,ch2),0)+1
        return bigramfreqdict
    
    def trigram_list_to_freqdict(self, trigram_list):
        trigramfreqdict=dict()
        for (ch1,ch2,ch3) in trigram_list:
            trigramfreqdict[(ch1,ch2,ch3)]=trigramfreqdict.get((ch1,ch2,ch3),0)+1
        return trigramfreqdict
    
    def ngram_freqdict_sorted(self, ngram_freqdict):
        ngramfreqdict_sorted=sorted(ngram_freqdict.items(), key=itemgetter(1), reverse=True)
        return ngramfreqdict_sorted
    
    def ngram_high_freq_result(self, ngram_freqdict_sorted):
        result_list = []
        texts = ''
        for (token, num) in ngram_freqdict_sorted:
            for text in token:
                texts = texts + text
            result_list.append((texts, num))
            texts =''
        return result_list