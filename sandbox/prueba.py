"""Simple network with two populations"""
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import pprint as pprint

import pylab as pl
import random as rd
import scipy as sp
import networkx as nx
import math as mt

##pprint anadido

"""Código de def_agentes, que genera y define los agentes de la población inicial en researchers (0)  y clinicians (1)."""


"""initiprob es el número que define la asignación del rol de investigadores o clínicos. El número es bajo para que haya una mayor probabilidad de que se den más investigadores que clínicos"""

identityprob = 0.3 

researcher = 0
clinicians = 1


"""Variables to follow-up k values for researchers-researchers, researchers-clinicians, and clinicians-researchers connections"""
timeData = []
ResRes = []
ResClin = []
ClinRes = []

rd.seed()

m = 1

def init():
    global time, net, RmaxNodeID, CmaxNodeID, positions, nextNet

    time = 0

    net = nx.erdos_renyi_graph(5, 0.03)

    for i in net.nodes_iter():
        if rd.random() > identityprob:
            net.node[i]['identity'] = researcher
        else:
            net.node[i]['identity'] = clinician
   
    RmaxNodeID = 4
    CmaxNodeID = 0

    positions = nx.random_layout(net)
    nextNetwork = net.copy()

def draw():
    pl.cla()
    nx.draw(net, pos = positions, node_color = [net.node[i]['identity'] for i in net.nodes_iter()], with_labels = False, edge_color = 'c', cmap = pl.cm.RdBu, vmin = 0, vmax = 1))
    pl.axis('image')
    pl.title('t = ' + str(time))
    plt.show()
    
net, nextNet = nextNet, net

import pycxsimulator
pycxsimulator.GUI().start(func = [init, draw, step])
