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
    global metadata, net, pos_old_net, citation_calendar, dates
    net = nx.Graph()
    
    metadata.bind = 'sqlite:///medline.sqlite'
    setup_all()

    citations = Citation.query.all() # filter(Citation.article_title.ilike(u"%cancer%")).all()

    # assemble calendar
    citation_calendar = {}
    for c in citations:
        if len(c.authors) > 0:
            if c.date_created in citation_calendar:
                citation_calendar[c.date_created][c.pmid] = c.authors
            else:
                citation_calendar[c.date_created] = {c.pmid: c.authors} 

    dates = citation_calendar.keys()
    dates.sort()
    pos_old_net = nx.layout.fruchterman_reingold_layout(net)



def draw(date):
    global net,pos_old_net
    pl.cla()
    pos_net = nx.layout.fruchterman_reingold_layout(net, pos=pos_old_net, iterations=11)
    nx.draw(net,
            pos = pos_net,
            node_size = [1 for n in net.nodes()],
            with_labels = False, edge_color = '#336699',
            node_color = '#000000',
            alpha=.5,)
#            cmap = pl.cm.RdBu, )
#            vmin = 0, vmax = 1)
    pl.axis('image')
    pl.title(str(date))
    plt.savefig('todo/'+str(date)+'.png')
    pos_old_net = pos_net


def step(date): 
    global net, citation_calendar, dates,  pos_old_net

    if date in citation_calendar:
        for pmid in citation_calendar[date]:
            for author1 in citation_calendar[date][pmid]:
                for author2 in citation_calendar[date][pmid]:
                    net.add_edge(author1, author2, pmid=pmid)






init()

#pprint.pprint(citation_calendar)
from datetime import datetime, timedelta

d1 = datetime(1998, 10, 23, 0, 0)
d2 = datetime(2002, 9, 28, 4, 0)

# # this will give you a list containing all of the dates
dd = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]

# for d in dd:
#     pprint.pprint( d)
#     step(d)
#     draw(d)
    

for date in dates:
    print date
    step(date)
    draw(date)
