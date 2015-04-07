# coding: utf-8

from pattern.en import parsetree
from pattern.vector import Document
import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt

def txt2tuples(text):
    s = parsetree(text, relations=True, lemmata=True)

    tuples = {}
    for e in s:
        d = Document(e)
        kw = d.keywords(top=15)
        nnp = []    
        for w in kw:
            if w[1].type == 'NNP':
                nnp.append(w[1].string)


        kw = d.keywords()
        words = []
        for w in kw:
            if w[1].type != 'NNP':        
                words.append(w[1].string)

        if len(nnp)>1:
            tuples[tuple(nnp)]=words.pop(0)

    return tuples




def tuples2graph(tuples):
    g = nx.Graph()
    for t in tuples:
        for pair in combinations(t,2):
            e = g.get_edge_data(*pair)

            if e:
                bow = e['bow']
                bow.add(tuples[t])
                g.add_edge(*pair, bow=bow)
            else:
                g.add_edge(pair[0], pair[1], bow=set([tuples[t],]))

    return g

text = open('data/theogony/theogony.txt').read()

G = tuples2graph(txt2tuples(text))

# pos = nx.spring_layout(G)
# #nx.draw(G)
# nx.draw_networkx_nodes(G,pos=pos,node_color='w',alpha=0.4)
# nx.draw_networkx_edges(G,pos=pos,alpha=0.4,width=1,edge_color='k')
# nx.draw_networkx_labels(G,pos=pos,fontsize=14)
# plt.savefig('red.svg')


nx.write_weighted_edgelist(G, 'red.csv')
