#This is a piece of code for generating a network using as input a
#dictionary file (dictionary.py).
### TO-DO: To generate a pickle
import networkx as nx
import matplotlib.pyplot as plt
import itertools as itools
from math import log, log10

def jaccard_index( first, *others ):
    return float( len ( first.intersection( *others ) ) )/ float( len( first.union( *others) ) )


# diccionario = {
#     'a': set([1,3,5]),
#     'b': set([1,2,5]),
#     }

diccionario={'Protomaya': set(['p','b','tap','tapg','t','tg','c','cg','cap','capg','cretr','cretrg','kpal','kpalg','k','kg','q','qg','s','sap','sretr','h','hw','x','xw','g','m','n','nvel','l','r','w','y','i','e','a','o','u']),'Achi':set(['p','b','cap','sap','capg','t','tg','c','cg','c','cg','cap','cg','k','kg','k','kg','q','g','s','sap','sap','sap','h','w','h','w','g','m','n','h','l','r','w','y','i','e','i','a','o','u']),'Aguacateco':set(['p','b','c','cg','c','capg','c','cg','cap','cretr','cretrg','cap','cretrg','capg','cretrg','k','kg','sap','k','kg','k','q','kg','qg','s','sap','sap','sretr''h','h','h','h','g','m','n','l','cretr','w','y','i','u','e','a','o','u']),'Cakchiquel':set(['p','b','cap','capg','t','c','cg','c','cg','cap','capg','k','kg','k','kg','q','kg','g','qg','s','sap','sap','s','sap','h','w','h','w','g','m','b','n','h','l','r','w','m','y','i','u','e','i','a','o','u']),'Chuj':set(['p','b','t','tg','t','cap','c','cg','c','cg','cap','cap','cap','cap','cg','cap','capg','k','kg','s','sap','h','h','h','h','g','m','n','nvel','l','r','y','w','y','i','e','a','o','u']),'Chol':set(['p','b','tap','tapg','c','cg','c','cg','cap','capg','cap','cap','cg','k','kg','k','kg','s','sap','sap','h','h','h','h','g','m','n','l','y','w','y','i','e','e','a','o','u']),'Chorti':set(['p','b','t','tg','t','cap','tg','capg','c','c','cg','cap','capg','tg','cap','cap','capg','cap','capg','k','s','sap','h','h','h','g','m','n','n','r','y','w','y','i','e','a','o','u']),'Huasteco':set(['p','b','t','tg','t','tg','dfs','t','c','cg','dfs','cap','tg','cg','cap','cretr','capg','cg','c','cg','k','kg','k','kg','dfs','sap','dfs','sap','h','w','h','w','g','m','w','n','y','h','l','y','w','y','i','e','e','a','o','u','u']),'Ixil':set(['p','b','c','cg','cap','capg','c','cg','cap','cap','cretr','cretrg','c''capg','cretrg','k','cretr','kg','k','kg','h','q','qg','s','sap','sretr','h','w','h','w','g','m','n','l','h','l','cap','w','y','i','e','a','o','u']),'Jacalteco':set(['p','b','t','tg','t','cap','c','cg','cap','cretr','cretrg','cap','cretr','capg','cretrg','k','kg','sap','cap','k','kg','x','q','kg','g','qg','s','sap','sretr','s','sap','sretr','h','h','x','x','g','m','n','nvel','l','y','w','y','i','e','e','a','o','u']),'Kekchi':set(['p','b','cap','capg','t','tg','c','s','cg','c','cg','cap','capg','k','k','kg','k','q','kg','qg','s','sap','sap','h','w','x','w','g','m','n','x','l','r','w','y','i','e','a','o','u']),'Yucateco':set(['p','b','cap','capg','tg','cap','capg','c','cap','t','cg','capg','cap','capg','cg','cap','capg','k','kg','sap','k','kg','k','kg','g','s','sap','sap','h','h','h','h','g','m','b','n','l','w','y','i','u','e','a','o','u','u']),'Mam':set(['p','b','c','t','cg','t','cap','c','cg','cap','cretr','capg','cap','cretr','capg','cretrg','k','cap','k','kg','k','q','qg','s','sap','s','sap','sretr','sretr','h','h','hw','h','h','g','m','n','l','h','l','cap','w','y','i','e','a','o','u']),'Mop':set(['p','b','c','cg','s','sap','h','g','m','n','h','n','l','y','w','m','y','i','e','a','o','u']),'Pocomchi':set(['p','b','cap','capg','t','tg','c','s','cg','c','cg','cap','capg','k','kg','k','kg','q','qg','s','sap','sap','sap','h','h','x','x','g','m','n','p','n','l','x','l','r','r','w','y','i','e','e','i','a','o','u']),'Pocomam':set(['p','b','cap','capg','t','tg','c','cg','c','cg','cap','capg','k','kg','k','kg','q','qg','s','sap','sap','h','h','x','x','g','m','n','n','x','l','r','w','y','i','e','e','i','a','o','u']),'Tzeltal':set(['p','b','t','tg','t','tg','c','s','cg','c','cg','cap','capg','cap','cap','capg','k','kg','k','kg','s','s','sap','sap','h','h','h','h','g','m','n','n','l','r','y','w','b','y','i','e','a','o','u']),'Quechua':set(['p','b','cap','capg','t','tg','c','cg','c','cg','cap','capg','k','kg','k','kg','q','qg','s','sap','sap','sap','h','w','h','w','g','m','n','l','h','l','r','w','y','i','e','i','a','o','u'])}


def network_from_dict( diccionario, threshold ):
    G = nx.Graph()

    for pair in itools.combinations( diccionario.keys(), 2 ):
        source = pair[0]
        target = pair[1]
        jin = jaccard_index( diccionario[source], diccionario[target] )
        if jin >= threshold:
            G.add_edge( source, target, jin = jin)

    return G

h = network_from_dict( diccionario, 0.9 )
#nx.draw(h)
jinx = []
for e in h.edges():
    jinx.append(h.get_edge_data(*e)['jin'])
plt.cla
njinx = [n*10 for n in jinx]
EdgeWidth = [log(n,2) for n in njinx]                
NodeSize = [2**h.degree(n) for n in nx.nodes(h)]
pos = nx.spring_layout(h)
nx.draw_networkx_labels(h, pos=pos)
nx.draw_networkx_nodes(h, pos=pos, node_size=NodeSize, label=True, alpha=0.75)
nx.draw_networkx_edges(h, pos=pos, width=EdgeWidth, alpha=0.75)


plt.show()



        
