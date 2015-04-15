
import argparse
import networkx as nx

parser = argparse.ArgumentParser(description='Interactive view of network')
parser.add_argument('--pickle', type=argparse.FileType('r'), required=True )
args   = parser.parse_args()

h = nx.read_gpickle( args.pickle )

for e in h.edges():
    print e[0],e[1],",".join(h.get_edge_data(*e)['bow'])
