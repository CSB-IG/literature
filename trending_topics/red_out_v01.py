#! /usr/bin/python
##Codigo para generar una red con el input de las redes sorted de los trending topics

import networkx as nx
import matplotlib.pyplot as plt
import os

os.chdir('/home/jmsiqueiros/Documentos/Trending_topics/Outcomes')

g = nx.read_edgelist('out00_sorted.csv')

g = nx.Graph(g)

g.remove_edges_from(g.selfloop_edges())

#nodeSize=[100*g.degree(n) for n in nx.nodes(g)]

pos=nx.spring_layout(g)

#nx.draw(g, pos=pos, node_size=nodeSize, alpha=0.75)

nx.draw(g, pos=pos, alpha=0.75)

plt.savefig("out00.png")

plt.show()
