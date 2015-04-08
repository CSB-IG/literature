import fileinput
import sys

for e in G.edges():
    print e[0],e[1],",".join(G.get_edge_data(*e)['bow'])
