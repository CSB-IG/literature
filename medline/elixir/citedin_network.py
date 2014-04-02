import pprint
import time, datetime

import random
random.seed()

import matplotlib
#matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import pylab as pl
import scipy as sp
import networkx as nx
import math as mt

from elixir import *
from models.medline import *
metadata.bind = 'mysql+oursql://caopsci:G@localhost/medline'
setup_all()



pos_old_net = {}
Ge          = nx.Graph()
citations   = Citation.query.filter( Citation.date_created>=datetime.date(1987,01,01),
                                     Citation.date_created<=datetime.date(2001,01,01) )
         

# create network from citedin links
for cited in citations:
    for citer in cited.cited_in:
        Ge.add_edge(cited, citer,
                    meshterms = set(
                        [mh.term for mh in cited.meshterms]
                        ).intersection(
                        set(
                            [mh.term for mh in citer.meshterms]) ) )


# drop small clusters
#Gcc=nx.connected_component_subgraphs(Ge)
#G=Gcc[0]
G=Ge

pl.cla()


#pos=nx.shell_layout(G)
#pos = nx.graphviz_layout(G,prog="wc")
#pos = nx.layout.fruchterman_reingold_layout(G, iterations=70, pos=pos)

# wow, que bonita grafica circular
pos =nx.graphviz_layout(G,prog='twopi', args='-Goverlap=scale -Gnodesep=70')

nodeSizes=[50*G.degree(n) for n in G.nodes()]


plt.figure(figsize=(30,30))
c = [cit.date_created.year for cit in G.nodes()]
nx.draw(G,       
        pos = pos,
        with_labels = False,
        node_size=nodeSizes,
        alpha=1,
        node_color=c,
        vmin=1987,
        vmax=2001,
        cmap=matplotlib.cm.summer,
        edge_color="lightgrey")


pl.axis('image')
pl.title('cited in')

plt.savefig("citedin/1987-2001.png", dpi=150)
#plt.savefig("citedin/2002.svg", dpi=150)



