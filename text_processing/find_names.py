import argparse
from pattern.es import parsetree
from pattern.vector import Document
from pprint import pprint
import networkx as nx

from operator import itemgetter
from itertools import groupby, combinations

parser = argparse.ArgumentParser(description='Find character names in text blobs. Create graph.')

parser.add_argument('--text', type=argparse.FileType('r'), required=True, help='find names here')
parser.add_argument('--names', type=argparse.FileType('r'), required=True, help='dictionary of names')
parser.add_argument('--pickle', type=argparse.FileType('w'), required=True, help='pickle to output graph')

args   = parser.parse_args()

last_names = [name.strip() for name in args.names.readlines()]

s = parsetree(args.text.read(), relations=True, lemmata=True)


def names_from_dict( nis ):
   
    names_in_sentence = nis.copy()
    indexes = names_in_sentence.keys()
    indexes.sort()

    names = []
    for k, g in groupby(enumerate(indexes), lambda (i,x):i-x):
        name = []
        for i in map(itemgetter(1), g):
            name.append(names_in_sentence[i])
        names.append(" ".join([n.capitalize() for n in name]))

    return names


all_sentences = {}
for i in range(len(s)):
    sentence = s[i]
    names_in_sentence = {}
    for n in range(1,len(sentence.words)):
        last_word = sentence.words[n-1]
        lw = last_word.string
        word = sentence.words[n]
        w = word.string

        if w.upper() in last_names and w[0].isupper() and len(w)>3 and lw.upper() in last_names and lw[0].isupper() and len(lw)>3:
            if not lw in names_in_sentence.values():
                names_in_sentence[last_word.index] = lw
            if not w in names_in_sentence:
                names_in_sentence[word.index] = w

    if len(names_in_sentence.keys()) > 1:
        all_sentences[i] = names_from_dict(names_in_sentence)



g = nx.Graph()

last_key = all_sentences.keys()[-1]
for i in range(last_key):

    # connect names in same sentence
    for pair in combinations(all_sentences.get(i,[]), 2):
        edge_data = g.get_edge_data(*pair)
        if edge_data:
            w = edge_data['w'] + 4
        else:
            g.add_edge(*pair, w=4)


    # connect names of sentence to names of next sentence
    for name1 in all_sentences.get(i,[]):
        for name2 in all_sentences.get(i+1,[]):
            edge_data = g.get_edge_data(name1, name2)
            if edge_data:
                w = edge_data['w'] + 3
            else:
                g.add_edge(name1, name2, w=3)


    # connect names of sentence to names of next to next sentence
    for name1 in all_sentences.get(i,[]):
        for name2 in all_sentences.get(i+2,[]):
            edge_data = g.get_edge_data(name1, name2)
            if edge_data:
                w = edge_data['w'] + 2
            else:
                g.add_edge(name1, name2, w=2)



    # connect names of sentence to names of next sentence
    for name1 in all_sentences.get(i,[]):
        for name2 in all_sentences.get(i+3,[]):
            edge_data = g.get_edge_data(name1, name2)
            if edge_data:
                w = edge_data['w'] + 1
            else:
                g.add_edge(name1, name2, w=1)
                
nx.gpickle.write_gpickle(g, args.pickle)
