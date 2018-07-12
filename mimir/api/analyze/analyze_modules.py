from api.preprocess.preprocess_modules import *

import itertools
import operator
from sklearn.feature_extraction.text import TfidfVectorizer

def get_words_pair(words_list: list, pair_length: int=2) -> dict:
    """Get tokens_list's words_pair.
    
    Args:
        words_list(list): List composed of words or tokens.
        pair_length(int): How many words in one pair.

    Returns:
        dict: A dict with words_pair: count.

    Examples:
        >>> print(get_words_pair(["今天", "天氣", "非常好"], 2))
        {('天氣', '非常好'): 1, ('天氣', '今天'): 1, ('非常好', '今天'): 1}

    """

    words_pair_dict = {}
    for pair in list(itertools.combinations(set(words_list), pair_length)):
        words_pair_dict[pair] = 1 
    return words_pair_dict

def get_multi_wordslist_coshow_words_pair(multi_wordslist: list, pair_length: int=2) -> dict:
    """Get wordslists' words pair. Could be used with the output of 'get_tfidf_each_words'.
    
    Args:
        multi_wordslist(list): A list of wordslists.
        pair_length(int): How many words in one pair.
        
    Returns:
        dict: A dict with words_pair: count.
        
    Examples:
        >>> print(get_multi_wordslist_coshow_words_pair([['火車'], ['火車', '美麗'], ['交通工具', '火車']], 2))
        {('火車', '美麗'): 1, ('交通工具', '火車'): 1}
        
        >>> print(get_multi_wordslist_coshow_words_pair([['火車'], ['火車', '美麗'], ['交通工具', '火車']], 1))
        {('火車',): 3, ('美麗',): 1, ('交通工具',): 1}
    """

    coshow_words_dict = {}
    for _list in multi_wordslist:
        for pair_tuple, count in get_words_pair(_list, pair_length).items():
            _ = tuple(sorted(pair_tuple))
            if _ in list(coshow_words_dict.keys()):
                coshow_words_dict[_] = coshow_words_dict.get(_) + 1
            else:
                coshow_words_dict[_] = count 
                
    return coshow_words_dict

def get_textslist_coshow_words_pair(text_list: str, content_language: str='ch') -> dict:
    """Get texts' words_pair.
    
    Args:
        text_list(list): List composed of texts.
        content_language(str): The tokenize_func's language, with 'en' or 'ch' choices.

    Returns:
        dict: A dict with words_pair:count.

    Examples:
        >>> print(get_textslist_coshow_words_pair( ["今天天氣好", "今天天氣差"]))
        Input text_list has 2 texts.
        Enumerating the 0 now.
        Finished.
        {('天氣', '好'): 1, ('今天', '天氣'): 2, ('今天', '好'): 1, ('天氣', '差'): 1, ('今天', '差'): 1}

    """
    print("Input text_list has {} texts.".format(len(text_list)))

    if check_content_language(content_language) == "en":
        tokenize_func = tokenize_en
    else:
        tokenize_func = tokenize_ch
          
    coshow_words_dict = {}
    for index, text in enumerate(text_list):
        if index % 50 == 0:
            print("Enumerating the {} now.".format(index))
        for pair_tuple, count in get_words_pair(tokenize_func(text)).items():
            _ = tuple(sorted(pair_tuple))
            if _ in list(coshow_words_dict.keys()):
                coshow_words_dict[_] = coshow_words_dict.get(_) + 1
            else:
                coshow_words_dict[_] = count 
    print('Finished.')
    
    return coshow_words_dict
    # return sorted(coshow_words_dict.items(), key=operator.itemgetter(1), reverse=True)

def transfer_coshow_words_dict_to_list(coshow_words_dict: dict) -> list:
    """Transfer coshow_words_dict to NetworkGraph edges format.
    
    Args:
        coshow_words_dict(dict): A dict with words_pair:count.
        
    Returns:
        list: A transfered output as type list.
        
    Examples:
        >>> print(transfer_coshow_words_dict_to({('交通工具', '火車'): 1, ('火車', '美麗'): 1}))
        get_multi_wordslist_coshow_words_pair([['火車', '美麗'], ['交通工具', '火車']], 2)
   
   
    """
    
    return sorted(coshow_words_dict.items(), key=operator.itemgetter(1), reverse=True)

def get_nodelist_from_pairsdict(pairs_dict: dict) -> list:
    """Collect all nodes of coshow_pairs_dict/pairs_dict into list. 

    Args:
        pairs_dict(dict): A dict with pairs_tuple.
    
    Returns:
        list: A nodes list.
    
    Examples:
        >>> print(get_nodelist_from_pairsdict({('交通工具', '火車'): 1, ('火車', '美麗'): 1}))
        ['交通工具', '火車', '美麗']

    """
    
    _list = []
    for pair_tuple, count in pairs_dict.items():
        _list.extend([node for node in pair_tuple])
        
    node_list = sorted(set(_list))
    return node_list

# check type hinting https://docs.python.org/3/library/typing.html
from typing import List
Keyslist = List[str] # Example: ["A", "B", "C"]

def transfer_spacesegtextslist_to_tfidfreadydict(space_seg_textslist: list, texts_title_list: Keyslist=[]) -> dict:
    """Create dict for tfidf use.
    
    Args:
        space_seg_textslist(list): A list with texts. Each text should be tokenized, and joined with space into str type.
        texts_title_list(list): A list with texts' title(str), default with [].
        
    Returns:
        dict: A dict combined with texts_title and space_seg_textslist.
        
    Examples:
        >>> print(transfer_spacesegtextslist_to_tfidfreadydict(['火車 快飛', '火車 好 美麗', '火車 是 交通 工具'], ["A", "B", "C"]))
        {'A': '火車 快飛', 'B': '火車 好 美麗', 'C': '火車 是 交通 工具'}
        
        >>> print(transfer_spacesegtextslist_to_tfidfreadydict(["Train is fast.", "Train is beautiful.", "Train is a transportation."]))
        {'0': 'Train is fast.', '1': 'Train is beautiful.', '2': 'Train is a transportation.'}
        
    """
    
    tfidf_ready_dict = {}
    
    # check space_seg_textslist's type
    if not isinstance(space_seg_textslist, list):
        raise TypeError("Error: type of space_seg_texts_list should be list.")

    # check texts_title_list's type
    if not isinstance(texts_title_list, list):
        raise TypeError("Error: type of texts_title_list should be list.")

    # ckeck length and create tfidf_ready_dict
    if texts_title_list:
        if (len(texts_title_list) == len(space_seg_textslist)):
            try:
                tfidf_ready_dict = {str(texts_title_list[i]): space_seg_textslist[i] for i in range(len(space_seg_textslist))}
            except ValueError:
                raise ValueError("failed to create tfidf_ready_dict")
        else:
            raise ValueError("space_seg_textslist' length is not equal to texts_title_list's length.")
    else:
        try:
            tfidf_ready_dict = {str(i): space_seg_textslist[i] for i in range(len(space_seg_textslist))}
        except TypeError:
            raise TypeError("Error: failed to transfer_textslist_to_tfidfdict, please to check if the space_seg_texts_list is right.")
    
    return tfidf_ready_dict

def check_tfidf_threshold_value(min_tfidf: float, max_tfidf: float):
    """Check if the min_tfidf and the max_tfidf fit the range.
    
    Args:
        min_tfidf(float): The minimal TFIDF, range from 0 to 1. Must be smaller than max_tfidf.
        max_tfidf(float): The maximal TFIDF, range from 0 to 1. Must be larger than min_tfidf.
            
    Returns:
        Nothing, but will raise Error when parameters don't follow the rules.
    
    """
    
    if isinstance(min_tfidf, float) and isinstance(max_tfidf, float):
        pass
    else:
        try:
            min_tfidf = float(min_tfidf)
        except TypeError:
            raise TypeError("The type of min_tfidf should be float or int.")

        try:
            max_tfidf = float(max_tfidf)
        except TypeError:
            raise TypeError("The type of max_tfidf should be float or int.")
            
    if 0.0 <= min_tfidf < max_tfidf <= 1.0:
        pass
    else:
        raise ValueError("The minimum of min_tfidf is 0.0. The maximum of max_tfidf is 1.0. And min_tfidf must be smaller than max_tfidf.") 
    
def get_tfidf(tfidf_ready_dict, content_language: str="en", stop_words_txt_path: str="english", min_tfidf: float=0.0, max_tfidf: float=1.0):
    """Use sklearn TfidfVectorizer to explore words in texts.

    Args:
        tfidf_ready_dict(dict):  tfidf_ready_dict could be created by "transfer_textslist_to_tfidfreadydict" function.
        content_language(str): The language of texts, with choices 'en'(default) and 'ch'. 
        stop_word_path (str): If content_language == "ch", it's neccesary to specify the path of stop_words txt file.
        min_tfidf(float): The minimal TFIDF, range from 0 to 1.
        max_tfidf(float): The maximal TFIDF, range from 0 to 1.

    Returns:
        dict: A dictionary of dictionaries, contains TFIDF of each documents.
        
    Examples:
        >>> print(get_tfidf({'A': 'Train is fast.', 'B': 'Train is beautiful.', 'C': 'Train is a transportation.'}, "en", "english", 0.6, 1))
        {'A': {'fast': 0.86103699594397642}, 'B': {'beautiful': 0.86103699594397642}, 'C': {'transportation': 0.86103699594397642}}
        
    """
    
    stop_words = []
    tfidf_dict = {}
    
    # Set stop_words for tfidf.
    if check_content_language(content_language) == "en":
        stop_words = "english"
    else:
        stop_words = get_stopwords_txt_to_list(stop_words_txt_path)

    # Check min_tfidf and max_tfidf
    check_tfidf_threshold_value(min_tfidf, max_tfidf)
    
    # Get tfidf_dict data
    try:
        titles_list = list(tfidf_ready_dict.keys())
        texts_list = list(tfidf_ready_dict.values())
    except TypeError:
        raise TypeError("Error: tfidf_ready_dict's type should be dict.")
    

    # Create sklearn TF-IDF vectorizer and fit the data   
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    tfidf = vectorizer.fit_transform(texts_list)
    tfidf_words_list = vectorizer.get_feature_names()

    for idx, title in enumerate(titles_list):
        tfidf_dict[title] = {}
        for _idx, word in enumerate(tfidf_words_list):
            if min_tfidf <= tfidf[idx, _idx] <= max_tfidf:
                tfidf_dict[title][word] = tfidf[idx, _idx]
                
    return tfidf_dict

def get_tfidf_total_words(tfidf_dict: dict) -> list:
    """Extract and collect all the words from tfidf_dict into one list.
    
    Args:
        tfidf_dict(dict): A tfidf_dict type, could created from 'get_tfidf' function. 

    Returns:
        list: A list with tfidf_dict's result words.
        
    Examples:
        >>> print(get_tfidf_total_words({'A': {'火車': 0.5, '美麗': 0.8}, 'B': {'交通工具': 0.8, '火車': 0.5}}))
        ['交通工具', '火車', '美麗']

    """
    
    tfidf_total_words_list = []
    for _v in tfidf_dict.values():
        for k, v in _v.items():
            tfidf_total_words_list.append(k)
    tfidf_total_words_list = list(set(tfidf_total_words_list))
    
    return tfidf_total_words_list # As network's node_list

def get_tfidf_each_words(tfidf_dict):
    """ Extract the words from tfidf_dict and collect each in list, then store in result output list.
    
    Args:
        tfidf_dict(dict): A tfidf_dict type, could created from 'get_tfidf' function. 
        
    Returns:
        list: A list with each tfidf_dict's result words_list.
        
    Examples:
        >>> print(get_tfidf_each_words({'A': {'火車': 0.5, '美麗': 0.8}, 'B': {'交通工具': 0.8, '火車': 0.5}}))
        [['火車', '美麗'], ['交通工具', '火車']]
    
    
    """
    
    each_words_list = []
    for _v in tfidf_dict.values():
        _list = []
        for k, v in _v.items():
            _list.append(k)
        each_words_list.append(_list)
        
    return each_words_list