#!/usr/bin/env python
import os
import sys
import pprint
import argparse
import pickle
import pylab as pl
import matplotlib.pyplot as plt
import networkx as nx

parser = argparse.ArgumentParser(description='Construct meshterm network for search criteria.')
parser.add_argument('--outfile', type=argparse.FileType('w'), required=True )
parser.add_argument('--pickle',  type=argparse.FileType('r'), required=True )

args    = parser.parse_args()
outfile = args.outfile
pickle_file  = args.pickle

if __name__ == '__main__':

    
    G = pickle.Unpickler(pickle_file).load()
    
    print "nodes: ", len(G.nodes())
      
    plt.cla()
    fig = plt.figure(figsize=(38,38), dpi=800)
    nx.draw(G, 
            node_size  = [G.degree(n) for n in G.nodes()],
            width      = [G.get_edge_data(*e)['citations'] for e in G.edges()],
            edge_color = [G.get_edge_data(*e)['jin'] for e in G.edges()] )
    plt.savefig( outfile )
