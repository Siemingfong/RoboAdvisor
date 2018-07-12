import os
import re 
import nltk
import jieba
import operator
import jieba.analyse
from nltk import ngrams
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

def remove_space_marks_ch(text: str, redundant_space_marks_list: list=["\n", "\r", "\t", " "]) -> str:    
    """Remove redundant space_marks in Chinese text.
    
    Args:
        text(str): The full text.
        redundant_space_marks_list(list): The redundant_space_marks_list setting.

    Returns:
        str: Return a redundant_space-removed text.

    Examples:
        >>> print(remove_space_marks_en("\t大家好，新年快樂。 \n"))
        大家好，新年快樂。

    """
    for mark in redundant_space_marks_list:
        text = re.sub(mark, '', text)
    return text 

def remove_space_marks_en(text: str, redundant_space_marks_list: list=["\n", "\r", "\t"]) -> str:    
    """Remove redundant space_marks in Englisth text.
    
    Args:
        text(str): The full text.
        redundant_space_marks_list(list): The redundant_space_marks_list setting.

    Returns:
        str: Return a redundant_space-removed text.

    Examples:
        >>> print(remove_space_marks_en("\t I love you, do you love me? \n"))
        I love you, do you love me? 

    """
    for mark in redundant_space_marks_list:
        text = re.sub(mark, '', text)
    return text

def cut_sentence_ch(text: str, cut_marks: str="，,;；.。！？!?") -> list:        
    """Cut text into sentences.
    
    Args:
        text(str): The full text.
        cut_marks(str): The end symbols of a sentence. Default to "，,;；.。！？!?"

    Returns:
        list: A list of all sentences.    

    Examples:
        >>> print(cut_sentence_ch("大家好，新年快樂"))
        ["大家好", "新年快樂"]

    """
    sentence_list = [text]
    for cut_mark in cut_marks:
        _list = []
        for sentence in sentence_list:
            _list.extend(sentence.split(cut_mark))
        sentence_list = _list
    return sentence_list

def cut_sentence_en(text :str) -> list:
    """Cut text into sentences.
    
    Args:
        text(str): The full text.

    Returns:
        list: A list of all sentences.    

    Examples:
        >>> print(cut_sentence_en("Hi, Jimmy. Happy new year."))
        ['Hi, Jimmy.', 'Happy new year.']

    """
    sent_tokenize_list = sent_tokenize(text)
    return sent_tokenize_list

def merge_deep_list(deep_list: list) -> list:
    """Merge 'lists in list' into list.

    Args:
        deep_list(list): List contains lists.
    
    Returns:
        list: Merged list.
            
    Examples:
        >>> merge_deep_list([["A", "B"], ["B", "C"]])
        ['A', 'B', 'B', 'C']
    
    """
    
    merged_list = []
    for _list in deep_list:
        merged_list.extend(_list)
    
    return merged_list

def create_dict_txt(file_path: str, word_info_list: list):
    """Create jieba_dictionary like txt file.

    Args:
        file_path(str): The target txt file path.
        word_info_list(list): example like [("帥哥", "1", "nz"), ("easy_list", "", "english"), ("希望", "nz")]
    
    """
    # Transfer word_info_list into _list for writing lines into txt
    _list =[]
    for word_info in word_info_list:
        word_info = list(word_info)
        assert (len(word_info) >= 1) and (len(word_info) <= 3), "word_info長度小於1或大於3，不符合新增字詞規則，請檢查。"
        word_info = ' '.join(w for w in word_info if w)
        _list.append(word_info + '\n')  
        
    # Clear the last word's '\n'
    # _list[-1] = re.sub('\n', '', _list[-1])
    
    # Write data
    try:
        f = open(file_path, "w", encoding='utf-8')
    except IOError:
        raise IOError("Error: 開啟或讀取文件失敗")     
    else:
        f.writelines(_list)
        f.close()

def delete_file(file_path: str):
    """Delete the target file.
    Args:
        file_path(str): The target txt file path.

    """
    try:
        os.remove(file_path)
    except IOError:
        raise IOError('fail to delete_file, please check file_path.')

def set_jieba_dictionary(dictionary_path):
    try:
        jieba.set_dictionary(dictionary_path)
        print('successfully set_jieba_dictionary')
    except:
        print('fail to set_jieba_dictionary')

def set_jieba_stop_words(file_path):
    try:
        jieba.analyse.set_stop_words(file_path)
        print('successfully set_jieba_stop_words')
    except:
        print('fail to set_jieba_stop_words')

def load_jieba_userdict(userdict_path):
    """ Use user-defined dictionary. """
    try:
        jieba.load_userdict(userdict_path)
        print('successfully load_jieba_userdict')
    except:
        print('fail to load_jieba_userdict')

def tokenize_ch(target_string: str) -> list:
    """Tokenize a Chinese string with jieba.lcut, return the tokens list.
    
    Args:
        target_string (str): The string meant to be tokenized.

    Returns:
        A list including all words in the target_sentence WITH stop words.
    
    """
    try:
        return jieba.lcut(target_string)
    except TypeError: 
        raise TypeError('fail to tokenize_ch')

def tokenize_en(target_string: str) -> list:
    """Tokenize a English sentence with nltk, return the tokens list.

    Args:
        target_string (str): The string meant to be tokenized.
    
    Returns:
        A list including all words in the target_sentence WITH stop words.
    """
    try:
        return word_tokenize(target_string)
    except TypeError: # Might not be correct Error
        raise TypeError('fail to tokenize_en')

def add_words_to_userdict(userdict_path: str, word_info_list: list):
    """Add a new-defined word to userdict_path like 'userdict.txt'.

    Args:
        userdict_path(str): The userdict txt file path.
        word_info_list(list): example like [("帥哥", "1", "nz"), ("easy_list", "", "english"), ("希望", "nz")]


    """
    if os.path.exists(userdict_path):
        # Check if the userdict_path exist
        try:
            f = open(userdict_path, "a", encoding="utf-8")
        except IOError:
            raise IOError("fail to open file with userdict_path, please check the userdict_path.")
        
        # Transfer word_info_list into _list for writing lines into txt
        _list =[]
        for word_info in word_info_list:
            word_info = list(word_info)
            assert (len(word_info) >= 1) and (len(word_info) <= 3), "word_info長度小於1或大於3，不符合新增字詞規則，請檢查。"
            word_info = ' '.join(w for w in word_info if w)
            _list.append(word_info + '\n')
            
        # Write word_info in new lines
        try:
            f.writelines(_list)
        except IOError:
            raise IOError("fail to write word_info to userdict_path.")
        else:
            print("successfully add_words_to_userdict")
            f.close()
        
    else:
        print("there's no such file with your userdict_path")

def ngram_en(target_string: str, n: int=2):
    """Generate patterns in n consecutive words of target_string.

    Args:
        target_string (str): The string meant to generate ngrams.
        n   (int, optional): The order of the language model (ngram size).

    Returns:
        A list containing n consecutive words of target_string.

    Examples:
        >>> ngram_en("SM is good!")
        ['SM is', 'is good', 'good !']
        >>> ngram_en("Algebra is the language of modern mathematics.", 3)
        ['Algebra is the', 'is the language', 'the language of', 'language of modern', 'of modern mathematics', 'modern mathematics .']

    """
    ngram_list = ngrams(tokenize_en(target_string), n)
    return [' '.join(gram) for gram in ngram_list]

def remove_punctuation(text: str, punctuation_list: list=['[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`，。{|}~「」＜＞〈〉《》【】（）？：、！+*＊“”]', '\n', '\xa0', ' ', '\u3000', '\u200b', '\t']) -> str:
    """Remove string's punctuations.
    
    Args:
        text(str): The full text.
        punctuation_list(list): Punctuation's list, default to ['[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`，。{|}~「」＜＞〈〉《》【】（）？：、！+*＊“”]', '\n', '\xa0', ' ', '\u3000', '\u200b', '\t']

    Returns:
        str: A punctuation-off string.

    Examples:
        >>> print(remove_punctuation("大家好，新年快樂^_^。"))
        大家好新年快樂

    """
    for punc in punctuation_list:
        text = re.sub(punc, '', text)
    return text

def get_tokens_count(tokens_list: list) -> dict:
    """Get basic tokens count informations.
    
    Args:
        tokens_list(list): List composed of tokens.

    Returns:
        dict: A dict with count of total_words and used_words(no repied).

    Examples:
        >>> print(get_tokens_count_ch(['新年', '新年', '快樂', '憂傷']))
        {'total_words': 4, 'used_words': 3}

    """
    tokens_count = {'total_words': len(tokens_list), 'used_words': len(set(tokens_list))}
    return tokens_count

def get_tokens_freqlist(tokens_list: list, min_freq: int=1, min_length: int=1) -> list:
    """Get basic tokens count informations.
    
    Args:
        tokens_list(list): List composed of tokens.
        min_freq(int): Minimum showing-frequence, default int=1.
        min_length(int): Minimum length of each token, default min_length=1

    Returns:
        list: A list with (token, freq) tuple.

    Examples:
        >>> print(get_tokens_freqlist_ch(['新年', '新年', '快樂', '憂傷'], 2, 1))
        [('新年', 2)]

    """
    sorted_tokens_freqdist = []
    _sorted_tokens_freqdist = sorted(nltk.FreqDist(tokens_list).items(), key = operator.itemgetter(1), reverse=True)   
    for (token, freq) in _sorted_tokens_freqdist:
        if freq >= min_freq and len(token) >= min_length:
            sorted_tokens_freqdist.append((token, freq))
    return sorted_tokens_freqdist

def get_stopwords_txt_to_list(stop_words_txt_path: str):
    stop_words_list = []
    try:
        with open(stop_words_txt_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                stop_words_list.append(line[:-1])
    except IOError:
        raise IOError("Error: 開啟或讀取文件失敗，請檢查文件路徑。")  
    else:
        return stop_words_list

def join_tokens_list_to_string(tokens_list: list, join_mark: str=" ") -> str:
    """Join list into string with join_mark.
    
    Args:
        tokens_list: List composed of tokens.
        join_mark: String type of marks or else.

    Returns:
        str: Mark-joined string.
                
    Examples:
        >>> print(join_tokens_list_to_string(['新年', '快樂', '大家', '好'], " "))
        新年 快樂 大家 好
        
    """
    try:
        return join_mark.join(tokens_list)
    except ValueError:
        raise ValueError("failed to join tokens_list")

def check_content_language(content_language: str) -> str:
    """Check input content_language
    
    Args:
        content_language(str): Should be 'en' or 'ch', or it will raise ValueError.
        
    Returns:
        str: 'en' or 'ch'
    
    Examples:
        >>> print(check_content_language('ch'))
        ch
        
        >>> print(check_content_language('en'))
        en
        
        >>> print(check_content_language('jp'))
        ValueError: The value of content_language should be 'ch' or 'en'.
    
    """
    if remove_punctuation(content_language.lower()) == 'en':
        return "en"
    elif remove_punctuation(content_language.lower()) == 'ch':
        return "ch"
    else:
        raise ValueError("The value of content_language should be 'ch' or 'en'.")     
