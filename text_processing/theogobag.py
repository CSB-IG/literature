# coding: utf-8

import fileinput
import sys
from pattern.en import parsetree
from pattern.vector import Document
import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt


# returns a dictionary, pairs of NNPs are the keys, keywords the value
def nnps_and_keywords(text):
    s = parsetree(text, relations=True, lemmata=True)

    nnp_kw = {}
    for e in s:
        d = Document(e)
        kw = d.keywords()

        nnp = set()
        for w in kw:
            if w[1].type == 'NNP':
                wdstr = []
                for wd in w[1].phrase.words:
                    if wd.type == 'NNP':
                        wdstr.append(wd.string)
                nnp.add("-".join(wdstr))


        kw = d.keywords(top=5)
        words = set()
        for w in kw:
            if w[1].type != 'NNP':
                if w[1].lemma:
                    words.add(w[1].lemma)
                else:
                    words.add(w[1].string)

        if len(nnp)>1 and len(words)>1:
            if tuple(nnp) in nnp_kw:
                nnp_kw[tuple(nnp)].update(words)
            else:
                nnp_kw[tuple(nnp)]=words

    return nnp_kw




def tuples2graph(tuples):
    g = nx.Graph()
    for t in tuples:
        for pair in combinations(t,2):
            e = g.get_edge_data(*pair)
            if e:
                bow = e['bow']
                bow.add(tuples[t])
                g.add_edge(pair[0], pair[1], bow=bow)
            else:
                g.add_edge(pair[0], pair[1], bow=tuples[t])

    return g

text = ""
for line in fileinput.input():
    text += "\n" + line

G = tuples2graph(nnps_and_keywords(text))

nx.write_gpickle(G, sys.stdout)
