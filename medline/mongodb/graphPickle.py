import cPickle as pickle
import networkx as nx
import matplotlib as mplot
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Graph article network')
parser.add_argument('--infile', type=str, required=True)
parser.add_argument('--outfile', type=str, required=True)
parser.add_argument('--threshold', type=int, required=True)

args    = parser.parse_args()
infile = args.infile
outfile = args.outfile
threshold = args.threshold

g = nx.gpickle.read_gpickle(infile)
pos = nx.spring_layout(g)

for i in g.edges(data=True):
    if i[2]['weight']<=threshold:
        g.remove_edge(i[0], i[1])
        
nx.draw(g,pos,node_color='#A0CBE2',edge_color='black',width=1, edge_cmap=plt.cm.Blues, with_labels=True)

edge_labels=dict([((u,v,),d['weight'])
             for u,v,d in g.edges(data=True)])



nx.draw_networkx_edge_labels(g, pos, edge_labels)


mplot.pyplot.savefig(outfile, dpi=500, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches=None, pad_inches=0.1)


