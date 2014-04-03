import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import pylab as pl
import random
import scipy as sp
import networkx as nx
import math as mt

from elixir import *
from models.medline import *
import time, datetime
import pprint


random.seed()

pos_old_net = {}


def init():
    global metadata, net, pos_old_net, citation_calendar, dates, date
    net = nx.Graph()
    
    metadata.bind = 'sqlite:///medline.sqlite'
    setup_all()

    citations = Citation.query.filter(Citation.article_title.ilike(u"%cancer%")).all()

    # assemble calendar
    citation_calendar = {}
    for c in citations:
        if len(c.authors) > 0:
            if c.date_created in citation_calendar:
                citation_calendar[c.date_created][c.pmid] = c.authors
            else:
                citation_calendar[c.date_created] = {c.pmid: c.authors} 

    dates = citation_calendar.keys()
    dates.sort(reverse=True)
    date = dates[-1]
    pos_old_net = nx.layout.fruchterman_reingold_layout(net)

# init()
# nx.draw(net)
# pl.show()


def draw():
    global net,pos_old_net,date
    pl.cla()
    pos_net = nx.layout.fruchterman_reingold_layout(net, pos=pos_old_net, iterations=11)
    nx.draw(net,
            pos = pos_net,
            node_size = [1 for n in net.nodes()],
            with_labels = False, edge_color = 'c', )
#            cmap = pl.cm.RdBu, )
#            vmin = 0, vmax = 1)
    pl.axis('image')
    pl.title('t = ' + str(date))
    plt.show()
    pos_old_net = pos_net


def step(): 
    global net, citation_calendar, dates, date, pos_old_net

    date=dates.pop()
    
    for pmid in citation_calendar[date]:
        for author1 in citation_calendar[date][pmid]:
            for author2 in citation_calendar[date][pmid]:
                net.add_edge(author1, author2, pmid=pmid)            

import pycxsimulator
pycxsimulator.GUI.timeInterval = 0
pycxsimulator.GUI().start(func = [init, draw, step])

