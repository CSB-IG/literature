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
time = []
net = nx.Graph()

def init():
    global time, net, metadata, day

    metadata.bind = 'sqlite:///medline.sqlite'
    setup_all()

    # get all distinct dates from citation table
    time = [c.date_created for c in Citation.query.all()]
    time = set(time)
    time = list(time)
    time.sort(reverse=True)
    day = time[-1]


init()


#nx.draw(net)
#pl.show()


def draw():
    global day
    pl.cla()
    nx.draw(net,
            pos = nx.fruchterman_reingold_layout(net),
            with_labels = True, edge_color = 'c',
            cmap = pl.cm.RdBu,
            vmin = 0, vmax = 1)
    pl.axis('image')
    pl.title('t = ' + str(day))
    plt.show() 


def step(): 
    global time, net, day

    # one day at a time
    day = time.pop()

    # fetch citations for that day
    for cit in Citation.query.filter_by(date_created=day).all():
        # add authors as nodes to the network
        for author in cit.authors:
            net.add_node(author)

        # add edges
        for author1 in cit.authors:
            for author2 in cit.authors:
                net.add_edge(author1, author2)                
            

import pycxsimulator
pycxsimulator.GUI().start(func = [init, draw, step])
