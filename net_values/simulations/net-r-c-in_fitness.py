# Basic network growth simulation in Python. The simulation is of two populations -researchers and clinicians-. 
# The simulation is based on a rule of exchange of samples for authorship. Each node has a fitness 
# according to their access to samples and their number of collaborators.

# This simulations is based on "Network Synchronization in the Kuramoto model" written by Hiroki Sayama, 
# and it can be found in PyCX.

# 2013/03/15

# JM. Siqueiros-Garcia
# R. Garcia-Herrera

# jsiqueiros@inmegen.gob.mx

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import pylab as pl
import random as rd
import scipy as sp
import networkx as nx
import math as mt

researcher = 0
clinician = 1




rd.seed()

m = 1

def init():
    global time, net, RmaxNodeID, CmaxNodeID, positions,nextNet, res, clin, nds
    
    time = 0
    
    net = nx.DiGraph()
    clin=['a','b','c','d','e']
    res=range(5)

    net.add_nodes_from(clin)
    for n in clin:
        net.node[n]['id']=clinician
 
    net.add_nodes_from(res)	
    for m in res:
        net.node[m]['id']=researcher
    net.add_edges_from([(0,'a'),(0,0),(1,'b'),(1,1),(2,'c'),(2,2),(3,'d'),(3,3),(4,'e'),(4,4)])
    

    RmaxNodeID = 4
    CmaxNodeID = 'e'

init()

positions = nx.random_layout(net)


#nx.draw(net)
#pl.show()


def draw():
    pl.cla()
    nodeSize=[1000*net.in_degree(n) for n in nx.nodes(net)]
    nx.draw(net, pos = positions, node_color = [net.node[i]['id'] for i in net.nodes_iter()], with_labels = True, edge_color = 'c', cmap = pl.cm.RdBu, vmin = 0, vmax = 1,node_size=nodeSize, alpha=0.75)
    pl.axis('image')
    pl.title('t = ' + str(time))
    plt.show() 


def fitness(nodes):
    global fit
    for i in res:
        for j in net.neighbors(i):
            net.node[i]['ws'] = (float(1)/net.in_degree(i))*net.degree(j)


    for i in clin:
        net.node[i]['ws']= net.degree(i)


    fit = []
    for n in net.nodes():
        fit.append(net.node[n]['ws'])



def roulette(nodes, fitness):
    fit_samples_sum = float(sum(fitness))
    probabilities = [float(x)/fit_samples_sum for x in fitness]
    ran = rd.random()
    s = 0.0
    for k in xrange(len(nodes)):
        s += probabilities[k]
        if ran <= s:
            break
    return nodes[k]


#roulette(net.nodes(), fit)



def step(): 
    global time, net, RmaxNodeID, positions, nds
    
    time += 1 
    
    RmaxNodeID += 1
    res.append(RmaxNodeID)
    net.add_node(RmaxNodeID)
    net.add_edge(RmaxNodeID, RmaxNodeID)
    net.node[RmaxNodeID]['id']=researcher
    net.node[RmaxNodeID]['ws']= 0
    nds = net.nodes()
    fitness(nds) #Si acomodo la funcion aqui, entonces el nuevo nodo no tiene asignada una 'ws' y la sim no corre.
    positions[RmaxNodeID] = sp.array([rd.gauss(0, 0.01), rd.gauss(0, 0.01)])

    for i in xrange(m): 
        target=roulette(nds, fit)
        net.add_edge(RmaxNodeID, target)

    #fitness(nds) #Si acomodo la funcion aqui, fit se genera despues de su llamada (roulette(nds,fit)) y la sim no corre.
    
    #positions = nx.spring_layout(net, pos = positions, iterations = 2) original layout
    positions = nx.random_layout(net)

import pycxsimulator
pycxsimulator.GUI().start(func = [init, draw, step])
