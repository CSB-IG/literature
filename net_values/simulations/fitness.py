#!python

"""Fitness method"""

import networkx as nx

researchers = [n for n, d in net.nodes(data=True) if d['id']==0]

clinicians = [n for n, d in net.nodes(data=True) if d['id']==1]

def ws():
	fitness_ws=net.node[node]['ws']=[net.in_degree(node)*float(1)/net.in_degree(j) for node in researchers for j in net.neighbors(node)]
	return fitness_ws
a=ws()

def cw():
	for node in net.nodes():
		fitness_cw= net.node[node]['cw']=[net.degree(i) for i in clinicians]
		return fitness_cw
b=cw()

""" Para incluirlo en el codigo de la simulacion en lugar de tenerlo como un metodo externo.
def w(a, b):
	fitness=a+b
	return fitness

def fitness():
    def ws():
        fitness_ws=net.node[node]['ws']=[net.in_degree(node)*float(1)/net.in_degree(j) for node in researchers for j in net.neighbors(node)]
        return fitness_ws
    a=ws()
    def cw():
        for node in net.nodes():
            fitness_cw= net.node[node]['cw']=[net.degree(i) for i in clinicians]
            return fitness_cw
        b=cw()
    def w(a, b):
        fitness=a+b
        return fitness
    c=w(a,b)
"""
