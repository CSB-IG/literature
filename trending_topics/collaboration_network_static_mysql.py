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


class TimeLapse():
    
    def __init__(self):
        # initialize database
        global metadata
        metadata.bind = 'mysql+oursql://caopsci:G@localhost/medline'
        setup_all()

        random.seed()

        # initialize network vars
        self.G = nx.Graph()
        self.pos_old_net = {}

        
        # since we wish analyze a lapse of time
        # we start by creating one, from a specific query

        review = PubType.get_by(pub_type=u'Review')
        citations = Citation.query.filter(Citation.pub_types.contains(review)).all()
        
        lapse = [c.date_created for c in citations]
        lapse = set(lapse)
        self.lapse = list(lapse)
        self.lapse.sort()

        # initial current date
        self.date = self.lapse[0]

        # colormap from countries
        countries = [j.country for j in Journal.query.all()]
        countries = set(countries)
        self.countries = list(countries)



    def draw(self):
        pl.cla()

        pos_net = nx.layout.fruchterman_reingold_layout(self.G,
                                                        pos=self.pos_old_net,
                                                        iterations=33)

        acarnevale = Author.get(141821)
        if acarnevale in self.G.nodes():
            pos_net[acarnevale] = [1,.001]
            pos_net = nx.layout.fruchterman_reingold_layout(self.G,
                                                            pos=pos_net,
                                                            fixed=[acarnevale,],
                                                            iterations=33)


        colors=[self.countries.index(self.G.edge[edge[0]][edge[1]]['cit'].country()) for edge in self.G.edges()]

        
        nx.draw(self.G,
                pos = pos_net,
                with_labels = False,
                node_color = 'white',
                node_alpha=.005,
                node_size=0,
                edge_color = colors,
                edge_cmap = plt.cm.Dark2,)
        pl.axis('image')
        pl.title(str(date))
        plt.savefig(str(date)+'.png')
        pos_old_net = pos_net

    def step(self): 
        # next current date
        self.date = self.lapse.pop()

        # fetch citations for that date
        for cit in Citation.query.filter_by(date_created=date).all():
            # add edges
            for author1 in cit.authors:
                for author2 in cit.authors:
                    self.G.add_edge(author1, author2, attr_dict={'cit': cit})

        self.G.remove_edges_from(self.G.selfloop_edges())
        
        for author in self.G.degree():
            if tl.G.degree()[author] < 3:
                self.G.remove_node(author)
                





tl = TimeLapse()

for date in tl.lapse:
    print date
    tl.step()
    tl.draw()
