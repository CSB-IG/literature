import argparse
import networkx as nx
import json
from itertools import combinations


parser = argparse.ArgumentParser(description='JSON sentence name dictionaries to NX graph')

parser.add_argument('--json', type=argparse.FileType('r'), required=True, help='name-sentence dictionaries')
parser.add_argument('--pickle', type=argparse.FileType('w'), required=True, help='pickle to output graph')

args   = parser.parse_args()

all_sentences = json.load(args.json)

from pprint import pprint

g = nx.Graph()

last_key = int(all_sentences.keys()[-1])
for i in range(last_key):
    # connect names in same sentence
    for pair in combinations(all_sentences.get(str(i),[]), 2):
        edge_data = g.get_edge_data(*pair)
        if edge_data:
            w = edge_data['w'] + 4
        else:
            w = 4
        g.add_edge(*pair, w=w)


    # connect names of sentence to names of next sentence
    for name1 in all_sentences.get(str(i),[]):
        for name2 in all_sentences.get(str(i+1),[]):
            edge_data = g.get_edge_data(name1, name2)
            if edge_data:
                w = edge_data['w'] + 3
            else:
                w = 3
            g.add_edge(name1, name2, w=w)


    # connect names of sentence to names of next to next sentence
    for name1 in all_sentences.get(str(i),[]):
        for name2 in all_sentences.get(str(i+2),[]):
            edge_data = g.get_edge_data(name1, name2)
            if edge_data:
                w = edge_data['w'] + 2
            else:
                w = 2
            g.add_edge(name1, name2, w=w)



    # connect names of sentence to names of next sentence
    for name1 in all_sentences.get(str(i),[]):
        for name2 in all_sentences.get(str(i+3),[]):
            edge_data = g.get_edge_data(name1, name2)
            if edge_data:
                w = edge_data['w'] + 1
            else:
                w = 1
            g.add_edge(name1, name2, w=w)
                
nx.gpickle.write_gpickle(g, args.pickle)
