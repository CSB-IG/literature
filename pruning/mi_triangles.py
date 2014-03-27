import networkx as nx
import itertools
import matplotlib.pyplot as plt


G = nx.Graph()

G.add_edges_from([(1,2,{'w': 6}),
                  (2,3,{'w': 3}),
                  (3,1,{'w': 4}),
                  (2,4,{'w': 2}),
                  (4,3,{'w': 3}),


              ])



import pprint


# detect triangles
triangles = []
for trio in itertools.combinations(G.nodes(), 3):
    vertices = []
    for v in itertools.combinations(trio, 2):
        vertice = G.get_edge_data(*v)
        if vertice:
            vertices.append(v)

    if len(vertices)==3:
        triangles.append(vertices)

pos = nx.spring_layout(G)
nx.draw(G,
        pos=pos,
        node_size  = [G.degree(n) for n in G.nodes()],
        width      = [G.get_edge_data(*e)['w'] for e in G.edges()],
        edge_color = [G.get_edge_data(*e)['w'] for e in G.edges()] )

plt.show()



for t in triangles:
    weights = {}
    for v in t:
        k = (G.get_edge_data(*v)['w'])
        weights[k]=v

    l = weights.keys()
    if len(l) != 1:
        l.sort()
        l.reverse()
        pprint.pprint(l)
        quitar = l.pop()
        G.remove_edge(*weights[quitar])


nx.draw(G,
        pos=pos,
        node_size  = [G.degree(n) for n in G.nodes()],
        width      = [G.get_edge_data(*e)['w'] for e in G.edges()],
        edge_color = [G.get_edge_data(*e)['w'] for e in G.edges()] )



plt.show()
