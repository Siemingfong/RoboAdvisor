from .getNER import *
import itertools


NE_Type = {
    "PERSON": 1,
    "ORGANIZATION": 2,
    "LOCATION": 3,
    "DATE": 4,
    "TIME": 5,
    "MONEY": 6,
    "PERCENT": 7,
    "FACILITY": 8,
    "GPE": 9,
    "GSP": 10
}

def get_NE_end(word, i, NE):
#     if(word[i+1][2].startswith('I-')):
    if(word[i+1][2] == 'I-{}'.format(NE)):
        return get_NE_end(word, i+1, NE)
    else:
        return i+1

def get_NEs_of_sent(sent):
    sent = sent + [('<END>', '<END>', '<END>')]
    
    NEs_of_sent = []
    for i in range(len(sent)-1):
        if(sent[i][2].startswith('B-')):
            NE = sent[i][2][2:]
            NE_end = get_NE_end(sent, i, NE) 
            NE_word = ' '.join([w for w, p, n in sent[i:NE_end]])
            NEs_of_sent.append((NE_word, NE))

    return NEs_of_sent

def containing_NE(NE, NEs_of_sent):
    return NE in [n for w, n in NEs_of_sent]

def find_NE(NE, NEs_of_sent):
    return [i for i, (w, n) in enumerate(NEs_of_sent) if n == NE]

def get_graph(text):
    textner = get_ner(text)

    NEs_of_sents = []
    for sent in textner:
        NEs_of_sent = get_NEs_of_sent(sent)
        NEs_of_sents.append(NEs_of_sent)
    
    all_nodes = [{"id": w, "group": NE_Type[n]} for sent in NEs_of_sents for w, n in sent]
    nodes = list({d['id']: d for d in all_nodes}.values())

    all_NE = [node['id'] for node in nodes]
    connection = {NE: {NE: 0 for NE in all_NE} for NE in all_NE}

    for sent in NEs_of_sents:
        if (sent):
            if (containing_NE('PERSON', sent)):
                people = [sent[i][0] for i in find_NE('PERSON', sent)]
                NE_words  = [w for w, n in sent]
                for i, j in itertools.product(people, NE_words):
                    connection[i][j] += 1
                        
            else:
                NE_words = [w for w, n in sent]
                for i, j in itertools.product(NE_words, repeat=2):
                    connection[i][j] += 1

    links = [{"source": source, "target": target, "value": value} for source, targets in connection.items() for target, value in targets.items()]
    graph = {"nodes": nodes, "links": links}

    return graph

if __name__ == '__main__':
    text = 'Alex is in Taipei. Alex hates Zucc. Alex is in Taipei. Mark is with Alex. Mark and Jack is in the Washington Monument. Taipei has Washington Monument. I am happy.'
    print(get_graph(text))