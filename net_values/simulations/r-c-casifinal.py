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
    net.add_edges_from([(0,'a'),(1,'b'),(2,'c'),(3,'d'),(4,'e')])
    
    nds = net.nodes()

    RmaxNodeID = 4
    CmaxNodeID = 'e'

init()

positions = nx.random_layout(net)


#nx.draw(net)
#pl.show()


def draw():
    pl.cla()
    nx.draw(net, pos = positions, node_color = [net.node[i]['id'] for i in net.nodes_iter()], with_labels = True, edge_color = 'c', cmap = pl.cm.RdBu, vmin = 0, vmax = 1)
    pl.axis('image')
    pl.title('t = ' + str(time))
    plt.show() 


for i in res:
    for j in net.neighbors(i):
        net.node[i]['ws'] = (float(1)/net.degree(i))*net.degree(j)


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

#fitness(nds, fit)



def step(): 
    global time, net, RmaxNodeID, positions
    
    time += 1 
    
    RmaxNodeID += 1 
    net.add_node(RmaxNodeID)
    net.node[RmaxNodeID]['id']=researcher 
    positions[RmaxNodeID] = sp.array([rd.gauss(0, 0.01), rd.gauss(0, 0.01)])

    for i in xrange(m): 
        target=roulette(nds, fit)
        net.add_edge(RmaxNodeID, target)
    
    positions = nx.spring_layout(net, pos = positions, iterations = 2)

import pycxsimulator
pycxsimulator.GUI().start(func = [init, draw, step])
