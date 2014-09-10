

import networkx as nx

import pylab as pl
import matplotlib.pyplot as plt


G = nx.Graph()

interacciones = open('/home/jespinal/literature/text_processing/SresNarco/RedPrueba2Full.txt').readlines()

for i in interacciones:
    campos  = i.split("\t")

    a=campos[1]
    b=campos[4].strip()
    
    if a != b:
        e = G.get_edge_data(a, b)

        if e:
            w = e['w']+1
            G.add_edge(a,b,w=w)
        else:
            G.add_edge(a,b,w=1)




            
narcodict = {}

i = 0
for n in G.nodes():
    narcodict[n] = i
#    print "%s,%s" % (i,n)
    i+=1




H = nx.Graph()
for i in interacciones:
    campos  = i.split("\t")

    a=campos[1]
    b=campos[4].strip()


    if (a in narcodict and b in narcodict) and (narcodict[a] != narcodict[b]):
        e = H.get_edge_data(narcodict[a], narcodict[b])
    
        if e:
            w = e['w']+1
            H.add_edge(narcodict[a],narcodict[b],w=w)
        else:
            H.add_edge(narcodict[a],narcodict[b],w=1)

        

for e in H.edges():
    ed = H.get_edge_data(*e)
    print "%s,%s,%s" % (e[0],e[1],ed['w'])
