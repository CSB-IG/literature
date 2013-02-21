def fitness():
	if net.node[i]['id']==0:
		
		ws = [float(1)/net.in_degree(i)*net.in_degree(j) for i in clinicians for j in researchers] #ws is for fitness gained for samples
		
	else:
		for n in net.nodes()cw=net.degree() #cw is for clinicians fitness


--------------------------------------------
"""This is for adding randomly an edge between the node of the group r to a node of the group c. The following is just an example. This part of code adds one edge at a time."""

g=nx.DiGraph()

r= ['a','b','c']
c= [1,2,3]

g.add_nodes_from(r)
g.add_nodes_from(c)

for n in rd.choice(r):
    g.add_edge(n, rd.choice(c))

----------------------------------------------------------"""Next task: check def roulette(). What I have to do is to test the following:

def roulette():
 	bla
		bla
			bla
def step():
targets = net.degree()keys()
preferences = [d for d in net.degree().values()] #In my case preferences are defined by fitness which depends of the degree.
target= roulette(targets, preferences)

"""

def roulette(options, w): # w is for fitness. In Hiroki's is weights.
fit_samples_sum = float(sum(w))
	if fit_samples_sum == 0.0
		fit_samples_sum == 1.0
	probabilities = [float(x)/fit_samples_sum for x in ws]
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
    preferences = [d for d in network.degree().values()]
    # the first "d" could be varied to, e.g., 1, 1/d, d ** 2, etc.

    maxNodeID += 1
    network.add_node(maxNodeID)
    positions[maxNodeID] = SP.array([RD.gauss(0, 0.01), RD.gauss(0, 0.01)])

    for i in xrange(m):
        target = roulette(targets, preferences)
        network.add_edge(maxNodeID, target)

    positions = NX.spring_layout(network, pos = positions, iterations = 2)
