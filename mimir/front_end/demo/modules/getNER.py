import nltk

import json


def testt(text):
    return text[:10]


def preprocess(text):
    """ Tag a english text with pos

    Args:
        text (str): The target text.

    Returns:
        pos_sents (list): A list of lists of tuples, containing each sentence with word-pos pairs.

    Examples:
    >>> text = "I am a loser. I don't have girlfriend."
    >>> preprocess(text)
    [
        [('I', 'PRP'), ('am', 'VBP'), ('a', 'DT'), ('loser', 'NN'), ('.', '.')],
        [('I', 'PRP'), ('do', 'VBP'), ("n't", 'RB'), ('have', 'VB'), ('girlfriend', 'NN'), ('.', '.')]
    ]
    """
    sentences = nltk.sent_tokenize(text)
    seg_sents = [nltk.word_tokenize(sent) for sent in sentences]
    pos_sents = nltk.pos_tag_sents(seg_sents)
    return pos_sents


def get_ner(text):
    """ Tag named-entities, return a json.

    Args:
        text (str): The target text.

    Returns:
        ner_sents (list): A list of lists of tuples, represented as conll format.
    """
    pos_sents = preprocess(text)
    ner_trees = nltk.ne_chunk_sents(pos_sents)
    ner_sents = [nltk.chunk.tree2conlltags(ner_tree) for ner_tree in ner_trees]
    return ner_sents


def ner_conll_to_json(ner_sents):
    """ Convert a conll-format ner_sents list to a json object. """
    ner_json = {
        "words": [w for sent in ner_sents for (w, p, n) in sent],
        "POS":   [p for sent in ner_sents for (w, p, n) in sent],
        "NE":    [n for sent in ner_sents for (w, p, n) in sent],
        "total_words": len([word for sent in ner_sents for word in sent])
    }
    return ner_json



# def ner_json_to_html(ner_json):
#     """ Convert a json object of ner info to html containing 'mark' tag 

#     Examples:
#     >>> text = "Alex go to Washington Monument. Hi Alex"
#     >>> ner_sents = get_ner(text)
#     >>> ner_json_text = ner_conll_to_json(ner_sents)
#     >>> print(ner_json_to_html(ner_json_text))
#     <mark data-entity="PERSON"> Alex </mark> go to <mark data-entity="GPE"> Washington </mark> Monument . Hi <mark data-entity="PERSON"> Alex </mark>
#     """
#     try:
#         ner = json.loads(ner_json)
#     except json.JSONDecodeError:
#         print('"ner_json" Decode Error')

#     ner_html = ""

#     for i in range(ner['total_words']):
#         word = ner['words'][i]
#         NE   = ner['NE'][i]

#         if NE.startswith('B-'):
#             ner_html += '<mark data-entity="{}"> '.format(NE[2:])

#         ner_html += word + " "
        
#         try:
#             next_NE = ner['NE'][>>>>> 675b11068f9624c124029488df14ff4fa186d93bi+1]
#         except:
#             if NE != 'O':
#                 ner_html += '</mark>'
#         else:
#             if NE != 'O':
#                 if not next_NE.startswith('I-'):
#                     ner_html += '</mark> '

#     return ner_html




if __name__ == '__main__':
    text = "Alex go to Washington Monument. Hi Alex"
    ner_sents = get_ner(text)
    ner_json_text = ner_conll_to_json(ner_sents)
    # print(ner_json_to_html(ner_json_text))
