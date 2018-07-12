# Django Modules
from django import template
from django.shortcuts import render_to_response, render
from django.http import Http404, HttpResponse,  JsonResponse

# # News-Info Modules
from .modules.PriceDataGet import *
from .modules.NewsDataGet import *
from .modules.StringAnalyzer import*
from .modules.SentenceAnalyzer import *
from .modules.TFIDFX import *
from .modules.NetworkGraph import *

# NER
from .modules.getNER import *
from .modules.NERnetwork import *

# Import Modules
import re
import os
import sys
import nltk
import json
import random
import jieba
import codecs
import jieba.analyse
import pymongo
import requests
import datetime
import operator
import itertools
import numpy as np
import pandas as pd
import networkx as nx
from networkx.readwrite import json_graph
from nltk import FreqDist
from pymongo import MongoClient
from dateutil.relativedelta import relativedelta
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer

# # PriceDataGet
P = None
price_df = {}
mark_price_cliff_list = []
mark_price_landmark_list = []

try:
    P = PriceDataGet(target_db='BTC_PRICE_DB',
                     target_collection='BTC_COINDESK_DAILY_PRICE_COLLECTION')
    P.mark_price_cliff()
    P.mark_price_landmark()
    P.price_df[['Datee', 'Close']].to_csv(
        './front_end/static/front_end/demo/static/custom/js/price_tsv.tsv', index=False, sep='	')
    price_df = json.dumps(list(P.price_df['Close']))
except:
    print("Retrieve price data failed")
else:
    # # Create Data for chart.js
    # price_df_label = json.dumps(list(datetime.datetime.strftime(
    #     n, "%Y-%m-%d") for n in P.price_df['Datee']))

    # # Create Mark_price_list for d3js price showing
    for item in P.price_tag_cliff[P.price_tag_cliff['Tag'] != 0].iterrows():
        t_dict = {'data': {'date': datetime.datetime.strftime(item[0], "%Y-%m-%d"),
                           'close': item[1]['Close']},
                  'dy': 5,
                  'dx': -70}
        mark_price_cliff_list.append(t_dict)

    for item in P.price_tag_landmark[P.price_tag_landmark['Tag'] != 0].iterrows():
        t_dict = {'data': {'date': datetime.datetime.strftime(item[0], "%Y-%m-%d"),
                           'close': item[1]['Close']},
                  'dy': 5,
                  'dx': -70}
        mark_price_landmark_list.append(t_dict)

"""
 # NewsDataGet
 N = NewsDataGet(target_client='mongodb://localhost:27017/',
                 target_db='BTC_NEWS_DB',
                 target_collection='BTC_TW_NEWS_COLLECTION')

 news_tag_by_cliff_3_3 = N.news_get_by_cliff(price_tag_cliff=P.price_tag_cliff,
                                             start_date_timedelta=-3,
                                             end_date_timedelta=3)
 news_tag_by_landmark_3_3 = N.news_get_by_landmark(price_tag_landmark=P.price_tag_landmark,
                                                   start_date_timedelta=-3,
                                                   end_date_timedelta=3)

 # # news data
 lm_tag_date = list(datetime.datetime.strftime(n, "%Y-%m-%d")
                 for n in list(news_tag_by_landmark_3_3['Markday']))
 lm_tag_num = list(news_tag_by_landmark_3_3['Newstag'])
 lm_news_date = list(datetime.datetime.strftime(n, "%Y-%m-%d")
                 for n in list(news_tag_by_landmark_3_3['Date']))
 lm_news_source = list(news_tag_by_landmark_3_3['Source'])
 lm_news_title = list(news_tag_by_landmark_3_3['Title'])
 lm_news_content = list(news_tag_by_landmark_3_3['Content'])

 landmark_json = {}
 landmark_json['data'] = []
 for i in range(len(lm_tag_date)):
     p_list = [lm_tag_date[i], lm_tag_num[i], lm_news_date[i], lm_news_source[i], lm_news_title[i], lm_news_content[i]]
     landmark_json['data'].append(p_list)

 cl_tag_date = list(datetime.datetime.strftime(n, "%Y-%m-%d")
                 for n in list(news_tag_by_cliff_3_3['Markday']))
 cl_tag_num = list(news_tag_by_cliff_3_3['Newstag'])
 cl_news_date = list(datetime.datetime.strftime(n, "%Y-%m-%d")
                 for n in list(news_tag_by_cliff_3_3['Date']))
 cl_news_source = list(news_tag_by_cliff_3_3['Source'])
 cl_news_title = list(news_tag_by_cliff_3_3['Title'])
 cl_news_content = list(news_tag_by_cliff_3_3['Content'])

 cliff_json = {}
 cliff_json['data'] = []
 for i in range(len(cl_tag_date)):
     p_list = [cl_tag_date[i], cl_tag_num[i], cl_news_date[i], cl_news_source[i], cl_news_title[i], cl_news_content[i]]
     cliff_json['data'].append(p_list)

 with codecs.open('./front_end/static/front_end/demo/static/custom/js/cliff.json', 'w', 'utf-8') as fp:
     json.dump(cliff_json, ensure_ascii = False, fp = fp)
 with codecs.open('./front_end/static/front_end/demo/static/custom/js/landmark.json', 'w', 'utf-8') as fp:
     json.dump(landmark_json, ensure_ascii = False, fp = fp)

"""

try:
    # StringAnalyzer()
    S = StringAnalyzer()

    # SentenceAnalyzer()
    SA = SentenceAnalyzer()

    # TFIDFX()
    TF = TFIDFX()
except:
    print('preprocess failed')


def text_analyze(request):
    # 輸入之文章
    if request.method == 'GET' and 'wanted_list' in request.GET:
        wanted_list = json.loads(request.GET['wanted_list'])

        for word in wanted_list:
            jieba.add_word(word)
            print('add word:{}'.format(word))

    if request.method == 'GET' and 'article' in request.GET:
        try:
            test_article = request.GET['article']

            # 顯示斷句且去除標點符號結果 -> list
            test_sentences = SA.sentences_splited_from_article(test_article)

            # 顯示分詞結果
            test_sentences_seg = []
            for sentence in test_sentences:
                test_sentences_seg.append(S.string_cutter(sentence)[0])

            # 顯示N-Gram(二和三)
            test_sentences_2_3_gram = []
            for sentence in test_sentences:
                test_sentences_2_3_gram.append(S.string_to_ngram(
                    sentence)[0] + S.string_to_ngram(sentence)[1])

            # 顯示文章基本統計
            dm_total_words = len(S.punctuation_cleaner(
                target_string=test_article))
            dm_used_words = len(
                set(S.punctuation_cleaner(target_string=test_article)))
            dm_total_segwords = S.string_cutter(
                S.punctuation_cleaner(target_string=test_article))[1][0][1]
            dm_used_segwords = S.string_cutter(
                S.punctuation_cleaner(target_string=test_article))[1][1][1]

            # 高頻字詞
            dm_hf_mix_words = S.string_cutter(S.punctuation_cleaner(
                target_string=test_article), high_freq_choice=2, word_text_count=1)[3]
            dm_hf_words = S.string_cutter(S.punctuation_cleaner(
                target_string=test_article), high_freq_choice=2, word_text_count=2)[3]
            dm_hf_ngram = S.string_to_ngram(
                S.punctuation_cleaner(target_string=test_article))[0][:19]
            dm_hf_coshow_words = SA.sentences_coshow_words_dict(
                target_batch_sentences_list=test_sentences)[:19]

            # 輸出Network
            # try:
            #     node_list = list(set([k1 for ((k1, k2), v) in dm_hf_coshow_words] + [k2 for ((k1, k2), v) in dm_hf_coshow_words]))
            #     edge_list = dm_hf_coshow_words
            #     NG = NetworkGraph()
            #     NG.ng_set_graph(target_node_list=node_list, target_edge_list=edge_list)
            #     dm_coshow_words_graph = json.dumps(NG.ng_graph_to_sigmaJs(output_json_option=False), ensure_ascii=False)
            # except:
            #     print('wrong')

            # NER

            ner = get_ner(test_article)
            ner_json = ner_conll_to_json(ner)
            # ner_html = ner_json_to_html(ner_json)

            graph_json = get_graph(test_article)
            # print(graph_json)

            # data to json
            data = json.dumps({'dm_sentences': test_sentences,
                               'dm_seg_words': test_sentences_seg,
                               'dm_sentences_2_3_gram': test_sentences_2_3_gram,
                               'dm_total_words': dm_total_words,
                               'dm_used_words': dm_used_words,
                               'dm_total_segwords': dm_total_segwords,
                               'dm_used_segwords': dm_used_segwords,
                               'dm_hf_mix_words': dm_hf_mix_words,
                               'dm_hf_words': dm_hf_words,
                               'dm_hf_2gram': dm_hf_ngram,
                               'dm_hf_coshow_words': dm_hf_coshow_words,
                               'ner': ner,
                               'ner_json': ner_json,
                            #    'ner_html': ner_html,
                               'graph_json': graph_json,
                               #    'dm_coshow_words_graph':dm_coshow_words_graph
                               }, ensure_ascii=False)

            return HttpResponse(data, content_type='application/json')
        except Exception as e:
            return HttpResponse('<h1>Something went wrong.</h1>', e)
    else:
        return render(request, 'demo/mf_text_mining.html', locals())


def intro(request):
    return render(request, 'demo/mf_intro.html')


def history(request):
    # graph data
    landmark_list = mark_price_landmark_list
    cliff_list = mark_price_cliff_list
    print(cliff_list)
    print(landmark_list)
    return render(request, 'demo/mf_history.html', locals())


def traffic_light(request):
    return render(request, 'demo/mf_traffic_light.html', locals())


def textmining(request):
    return render(request, 'demo/mf_text_mining.html', locals())
