import sys
import argparse
import networkx as nx
from itertools import combinations

parser = argparse.ArgumentParser(description='Interactive view of network')
parser.add_argument('--pickle', type=argparse.FileType('r'), required=True )
args   = parser.parse_args()

h = nx.read_gpickle( args.pickle )
g = nx.Graph()

for e in h.edges():
    for pair in combinations(h.get_edge_data(*e)['bow'], 2):
        g.add_edge(pair[0], pair[1])


nx.write_gpickle(g, sys.stdout)
