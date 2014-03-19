#This is a piece of code for generating a network using as input a
#dictionary file (dictionary.py).

import networkx as nx
import matplotlib as plt
import itertools as itools


def jaccard_index( first, *others ):
    return float( len ( first.intersection( *others ) ) )/ float( len( first.union( *others) ) )

values = []

for k in dictionary:
    values.append( set(dictionary.get( k ) ) )


G = nx.Graph()

keys = []

for nodes in dictionary:
    keys.append( nodes )
for pair in itools.combinations( keys, 2 ):
    source = pair[0]
    target = pair[1]
    e = G.get_edge_data( source, target )
    if not e:
        G.add_edge( source, target, jin = jaccard_index( *values ) )
    nx.draw(G)
    pl.show()



        
