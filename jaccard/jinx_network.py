#This is a piece of code for generating a network using as input a
#dictionary file (dictionary.py).
### TO-DO: To generate a pickle
import networkx as nx
import matplotlib as plt
import itertools as itools


def jaccard_index( first, *others ):
    return float( len ( first.intersection( *others ) ) )/ float( len( first.union( *others) ) )


diccionario = {
    'a': set([1,3,5]),
    'b': set([1,2,5]),
    }



def network_from_dict( diccionario, threshold ):
    G = nx.Graph()

    for pair in itools.combinations( diccionario.keys(), 2 ):
        source = pair[0]
        target = pair[1]
        jin = jaccard_index( diccionario[source], diccionario[target] )
        if jin >= threshold:
            G.add_edge( source, target, jin = jin)

    return G

h = network_from_dict( diccionario, 0.5 )
nx.draw(h)
pl.show()



        
