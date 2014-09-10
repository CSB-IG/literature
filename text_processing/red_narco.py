

import networkx as nx

import pylab as pl
import matplotlib.pyplot as plt


G = nx.Graph()

interacciones = open('/home/jespinal/literature/text_processing/SresNarco/RedPrueba2Full.txt').readlines()

for i in interacciones:
    campos  = i.split("\t")

    a=campos[1]
    b=campos[4].strip()
    
    e = G.get_edge_data(a, b)

    if e:
        w = e['w']+1
        G.add_edge(a,b,w=w)
    else:
        G.add_edge(a,b,w=1)




for e in G.edges():
    ed = G.get_edge_data(*e)
    print "%s,%s,%s" % (e[0],ed['w'],e[1])
    
# nx.draw(G, 
#         node_size  = [G.degree(n) for n in G.nodes()],
#         width      = [G.get_edge_data(*e)['w'] for e in G.edges()],
#         edge_color = [G.get_edge_data(*e)['w'] for e in G.edges()] )

# plt.show()

