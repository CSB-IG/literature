#!python

"""Fitness method"""
def ws():
	fitness_ws=g.node[node]['ws']=[g.in_degree(node)*float(1)/g.in_degree(j) for node in researchers for j in g.neighbors(node)]
	return fitness_ws
a=ws()

def cw():
	for node in net.nodes():
		fitness_cw=g.node[node]['ws']=[net.degree(i) for i in clinicians]
		return fitness_cw
b=cw()

def w(a, b):
	fitness=a+b
	return fitness
