import itertools
import networkx as nx
import pprint

# computes jacard index for two or mor sets
def jaccard_index(first, *others):
    return float( len( first.intersection(*others))) / float(len(first.union(*others)))


def mesh_network( cursor ):

    G = nx.Graph()

    for cit in cursor:
        keys = []
        for msh in cit['MH']:
            keys.append(msh)

        for pair in itertools.combinations( keys, 2 ):
            source = pair[0]
            target = pair[1]
                
            e = G.get_edge_data(source, target)

            if not e:
                G.add_edge(source, target, citations=[cit,])
            else:
                v = e['citations']
                v.append(cit)
                G.add_edge(source, target, citations=v)

    H = nx.Graph()
    for e in G.edges():
        edge_data = G.get_edge_data(*e)

        bags = [set(c['MH']) for c in edge_data['citations']]

        H.add_edge(e[0], e[1], jin=jaccard_index( *bags ), citations=len(edge_data['citations']))

    return H
