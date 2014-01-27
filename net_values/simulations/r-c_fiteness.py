"""Simple network with two populations. Preferential attachment by fitness"""
"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Notes:																						
% 1) This version is r-c_1_4_fitness.py in /Dropbox/Workinprogress/Proyectos/Net_Values/Simulation/
% 2) r_c-fitness stands for: r:researcher, c:clinician and this populations connect among them by preferential attachment
% according their fitness.
% 3) May be, eventually a limit on the number of connections for clinicians must be imposed.	
% Not even clinicians have unlimited access to biological samples.	
% 4) In the analysis part, look for the behavior of k in relation to the manner in which researchers and clinicians acquire 
% -- diferently-- their fitness. 
% 5) Everytime a node is added (by means of an edge) an identity has to be assigned and it has to be 
% added to the list of researchers or clinicians.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt

import pylab as pl
import random as rd
import scipy as sp
import networkx as nx
import math as mt


"""Codigo de def_agentes, que genera y define los agentes de la poblacion inicial en researchers (0)  y clinicians (1)."""


researcher = 0
clinician = 1


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

    net = nx.DiGraph()
	clin=['a','b','c','d','e']
	res=range(5)
    net.add_nodes_from(clin)
	for n in clin:
		net.node[n]['id']=clinician
	net.add_nodes_from(res)	
	for m n res:
		net.node[m]['id']=researcher
	net.add_edges_from([(0,'a'),(1,'b'),(2,'c'),(3,'d'),(4,'e')])
	
	"""Here I am adding 5 clinicians and 5 researcher. Each researcher will be connected to one clinician so to avoid the problem of dividing float(1)/net.in_degree(i), being i any clinician, when net.in_degree(i)=0 --because 1/0 cannot be done--. In connecting one researcher with one clinician, every clinician has a in_degree of one. """

	researchers = [n for n, d in net.nodes(data=True) if d['id']==0] """This is to making a list once an id has been already asigned to the node. This line makes a list of those nodes that are identity==0.""""
	clinicians = [n for n, d in net.nodes(data=True) if d['id']==1] """This is to making a list once an id has been already asigned to the node. This line makes a list of those nodes that are identity==1.""""
	"""An identity must be given to every node that is added to the network """
    
   # nx.draw(net) 
   # pl.show()
    RmaxNodeID = 1
   # CmaxNodeID = 1
    
    positions = nx.random_layout(net)
    nextNetwork = net.copy()


"""def draw() Checked on february 14, and everything fine"""
def draw():
    pl.cla()
    nx.draw(net, pos = positions, node_color = [net.node[i]['id'] for i in net.nodes_iter()], with_labels = True, edge_color = 'c', cmap = pl.cm.RdBu, vmin = 0, vmax = 1)
    pl.axis('image')
    pl.title('t = ' + str(time))
    plt.show()


"""if net.node[i]['id']==0:		
	ws = [float(1)/net.in_degree(i)*net.in_degree(j) for i in clinicians for j in researchers] 
ws is for fitness gained for samples. What is interesting is that because researchers --at point zero-- have an in_degree=0 and clincians an in_degree=1, the fitenss for researchers so far is zero which is 1/1*0= 0. This is because researchers have no fellows collaborators"""

for n in net.nodes():
	ws=[net.in_degree(n)*float(1)/net.in_degree(m) for n in researchers for m in net.neighbors(n)] #Falta arreglarla idea de fitness, porque qué sucede con aquellos researchers que no están conectados a ningún clinician.

for n in net.nodes():
	cw=[net.degree(i) for i in clinicians]
		 #cw is for clinicians fitness/ I just have made it into a list. It needs to be tested. The idea is to create a list of in_degrees for clinicians, since this is their fitness.

w = ws + cw #w stands for fitness. This merges the two fitness lists that will be introduced to def fitness(options, w) 

"""def roulette"""    
def roulette_r(options, w):# To be redefined including fitness, so it should be: (options, ws)
"""There is going to be only one roulette, based on one common variable called fitness --or w--. There are two options to explore: 1) when initial ws is 0 and cw is 1, clinicians have higher chances to get connected. 2) when initial ws=cw, then researchers and clinicians have equal chances to be selected in the roulette. FUNCTION ROULETTE WORKS FEBRUARY 25, 2013. OPTIONS ARE net.nodes(). I NEED TO EXPLAIN HOW DOES IT WORK BECUASE IN THE ORIGINAL PROGRAM EACH NODE HAS ITS OWN DEGREE AND THEY ARE RELATED IN THE FUNCTION AS: (options=net.degree().keys() targets=net.degree().values()). BUT MAY BE IN MY CASE THE LIST OF NODES IS SYMMETRICAL TO THE LIST OF ALL FITNESSES W."""    

	fit_samples_sum = float(sum(w))
	if fit_samples_sum == 0.0:
		fit_samples_sum == 1.0
	probabilities = [float(x)/fit_samples_sum for x in w]
	ran = rd.random()
	s = 0.0
	for k in xrange(len(options)):
		s += probabilities[k]
		if ran <= s:
			break
       return options[k]

def step():
    global time, network, maxNodeID, positions

time += 1

    targets = network.degree().keys()
    preferences = w #preferences = [d for d in network.degree().values()]
    # the first "d" could be varied to, e.g., 1, 1/d, d ** 2, etc.

    maxNodeID += 1
    network.add_node(maxNodeID)
    positions[maxNodeID] = SP.array([RD.gauss(0, 0.01), RD.gauss(0, 0.01)])

    for i in xrange(m):
        target = roulette(targets, preferences)
        network.add_edge(maxNodeID, target)

    positions = NX.spring_layout(network, pos = positions, iterations = 2)

import pycxsimulator
pycxsimulator.GUI().start(func = [init, draw, step])"""
