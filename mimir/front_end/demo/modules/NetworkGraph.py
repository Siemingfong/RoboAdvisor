# Import Modules
import re
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
import networkx as nx
from networkx.readwrite import json_graph
from nltk import FreqDist
from dateutil.relativedelta import relativedelta
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer

class NetworkGraph:
    """ 
        node_format/edge_list format
        ## node_list # ['string_1', 'string_2', 'string_3']
        ## edge_list # [(('string_1', 'string_2'), 2), (('string_1', 'string_3'), 2)]
    """
    def __init__(self):
        pass
    def ng_set_graph(self, target_node_list, target_edge_list):
        G = nx.MultiDiGraph() # Initial the NetworkX Entity
        for i in range(len(target_node_list)): # Add nodes data to G
            G.add_node(n=i, label=target_node_list[i])
        for i in range(len(target_edge_list)): # Add edges data to G
            G.add_edge(target_node_list.index(target_edge_list[i][0][0]), 
                       target_node_list.index(target_edge_list[i][0][1]),
                       id = i,
                       weight = target_edge_list[i][1])  
        G = G.to_undirected() # Make G undirected
        self.G = G
        
    def ng_draw_graph(self):
        pos =nx.spring_layout(self.G) # Get spring_layout's node (x,y)
        nx.draw_networkx(self.G, pos) # draw
        
    def ng_check_graph_info(self):
        return self.G.nodes(), self.G.edges()
    
    def ng_graph_to_sigmaJs(self, output_json_option=True, output_json_file = 'output.json'):
        degr = self.G.degree() # Get node's degree for node size set
        pos =nx.spring_layout(self.G) # Get spring_layout's node (x,y)
        fixNG = json_graph.node_link_data(self.G) # With networkx.readwrite 's json_graph to export the network info.
        fixNG['nodes'] = [
            {
                "id": node['id'],
                "label": node['label'],
                "x":pos[node['id']][0],
                "y":pos[node['id']][1],
                "size": degr[node['id']]
            } for node in fixNG['nodes']]
        fixNG['edges'] = [
            {
                "source": fixNG['nodes'][link['source']]['id'],
                "target": fixNG['nodes'][link['target']]['id'],
                "id": link['id']
            }
            for link in fixNG['links']]
        fixNG.pop('links', None) # Del the 'links' key
        #fixNG = str(json.dumps(fixNG, ensure_ascii=False)) # Stringifies the json
        if output_json_option == True:
            with codecs.open(output_json_file, 'w', 'utf-8') as fp:
                json.dump(fixNG, ensure_ascii = False, fp = fp)
            print('json file saved as {}'.format(output_json_file))
        return fixNG