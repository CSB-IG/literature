from django.db.models import Q
from medline.models import *
from random import shuffle
import json, itertools, datetime
import networkx as nx
import pprint




def plot(G, path):
    import pylab as pl
    import matplotlib.pyplot as plt
    import networkx as nx
    plt.cla()
    fig = plt.figure(figsize=(38,38), dpi=800)
    nx.draw(G, 
            node_size  = [G.degree(n)*10 for n in G.nodes()],
            width      = [G.get_edge_data(*e)['weight']*20 for e in G.edges()],
            edge_color = [G.get_edge_data(*e)['weight'] for e in G.edges()] )
    plt.savefig( path )


# format network as dict ripe for json
def citation_network2dict(G):
    nodes = []
    nodei = []
    for i,node in enumerate(G.nodes()):
        nodei.append(node)
        nodes.append( {"node": i,
                       "name": str(node.pmid),
                       "title": node.title,
                       "year": node.date_created.year,
                       "degree": G.degree(node)} )

    links = []
    for e in G.edges():
        links.append( {"source": nodei.index(e[0]),
                       "target": nodei.index(e[1]), } )


    net = {"nodes" : nodes,
           "links" : links }
    
    return net





def cited_in_network( criteria ):
    q_ob = Q()

    for term in criteria:
        q_ob |= Q(meshterms__term__icontains=term)
    
    citations = Citation.objects.filter(q_ob)

    G = nx.DiGraph()

    for cited in citations:
        # create network from citedin links
        for citer in cited.cited_in.all():
            if len(set(citer.major_terms()).intersection(set(cited.major_terms())))>0:
                G.add_edge( citer,
                            cited,
                            weight = len(set(cited.meshterms.all()).intersection(set(citer.meshterms.all()))))

    return G










def branch_network( year, roots):
    citations = Citation.objects.filter( date_created__year = year )

    G = nx.Graph()

    for cit in citations.all():
        keys = []
        for msh in cit.meshterms.all():
            for branch in msh.branch_set.all():
                if branch.root() in roots:
                    keys.append( ".".join(branch.branch.split('.')[:3]) )


        for pair in itertools.combinations( keys, 2 ):
            source = pair[0]
            target = pair[1]
                
            e = G.get_edge_data(source, target)
            if not e:
                G.add_edge(source, target, weight=1)
            else:
                G.add_edge(source, target, weight=e['weight']+1)
                    
    return G







def branch_network2hive(G):
    nodes = G.nodes()
    nodes.sort()

    # find roots
    roots = []
    for node in nodes:
        roots.append( node[:1] )
        roots = list(set( roots ))

    # place nodes on axes
    axes = {}
    for root in roots:
        axes[root] = []
        for node in nodes:
            if node[:1] == root:
                axes[root].append(node)

    # format nodes for hiveplot
    nodes = []
    x = 0
    for root in axes:
        y = 0
        delta = 1.0/len(axes[root])
        for branch in axes[root]:
            y += delta
            nodes.append( {'x': x, 'y': y, 'branch': branch} )
        x += 1

    nodes.sort()

    # positional keys for nodes
    noded = {}
    for i,node in enumerate(nodes):
        noded[node['branch']] = i
    
    edges = G.edges()
    edges.sort()

    links = []
    for edge in edges:
        links.append( {'source': nodes[noded[edge[0]]], 'target': nodes[noded[edge[1]]] } )
        

    net = {'nodes': nodes,
           'links': links,}
    return net





#def article_network( year ):
#    G = nx.Graph()
#    for msh in Meshterm.objects.all():
#        nodes = []
#
#        for cit in msh.citation_set.filter(date_created.year__eq=year):
#            nodes.append(cit)
#
#        for pair in itertools.combinations( nodes, 2 ):
#            source = pair[0]
#            target = pair[1]
#
#            e = G.get_edge_data(source, target)
#
#            if not e:
#                G.add_edge(source, target, weight=1)
#            else:
#                G.add_edge(source, target, weight=e['weight']+1)


#    return G




def term_diversity( year ):
    terms = []
    for cit in Citation.objects.filter( date_created__year = year ):
        for msh in cit.meshcitation_set.all():
            terms.append(msh.__unicode__())

    return len(set(terms))



def filter_by_weight( G, threshold ):
    g = nx.Graph()

    for e in G.edges():
        if G[e[0]][e[1]]['weight'] >= threshold:
            g.add_edge(e[0],e[1], weight=G[e[0]][e[1]]['weight'])

    return g


def filter_by_key( G, key, threshold ):
    g = nx.Graph()

    for e in G.edges():
        if G[e[0]][e[1]][key] >= threshold:
            g.add_edge(e[0],e[1], G.get_edge_data(e[0],e[1]))

    return g



def filter_by_weight_top( G, threshold ):
    g = nx.Graph()

    for e in G.edges():
        if G[e[0]][e[1]]['weight'] <= threshold:
            g.add_edge(e[0],e[1], weight=G[e[0]][e[1]]['weight'])

    return g




# computes jacard index for two or mor sets
def jaccard_index(first, *others):
    return float( len( first.intersection(*others))) / float(len(first.union(*others)))



# citations = Citation.objects.filter( date_created__year = year )
def mesh_network( citation_queryset ):

    G = nx.Graph()

    for cit in citation_queryset.all():
        keys = []
        for msh in cit.meshcitation_set.all():
            keys.append(msh)

        for pair in itertools.combinations( keys, 2 ):
            source = pair[0]
            target = pair[1]
                
            e = G.get_edge_data(source.majorless(), target.majorless())

            if not e:
                G.add_edge(source.majorless(), target.majorless(), citations=[cit,])
            else:
                v = e['citations']
                v.append(cit)
                G.add_edge(source.majorless(), target.majorless(), citations=v)

    H = nx.Graph()
    for e in G.edges():
        edge_data = G.get_edge_data(*e)
        # sets = []
        # for cit in v['citations']:
        #     sets.append(cit.bag_of_words())
        bags = [cit.bag_of_words() for cit in edge_data['citations']]

        H.add_edge(e[0], e[1], jin=jaccard_index( *bags ), citations=len(edge_data['citations']))


    return H



def author_network( citation_queryset ):
    G = nx.Graph()

    for cit in citation_queryset.all():
        keys = []
        for a in cit.authors.all():
            keys.append(a)

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

        H.add_edge(e[0], e[1], weight=len(edge_data['citations']))

    return H



# format network as dict ripe for json
def author_network2json(G):
    nodes = []
    nodei = []
    for i,node in enumerate(G.nodes()):
        nodei.append(node)
        nodes.append( {"node": i,
                       "name": node.name,
                       "degree": G.degree(node)} )

    links = []
    for e in G.edges():
        
        links.append( {"source": nodei.index(e[0]),
                       "target": nodei.index(e[1]),
                       "weight": G.get_edge_data(*e)['weight'] } )


    net = {"nodes" : nodes,
           "links" : links }


    return json.dumps( net )




# format network as dict ripe for json
def mesh_network2json(G):
    nodes = []
    nodei = []
    for i,node in enumerate(G.nodes()):
        nodei.append(node)
        nodes.append( {"node": i,
                       "name": node,
                       "degree": G.degree(node)} )

    links = []
    for e in G.edges():
        
        links.append( {"source": nodei.index(e[0]),
                       "target": nodei.index(e[1]),
                       "citations": G.get_edge_data(*e)['citations'],
                       "jin": G.get_edge_data(*e)['jin'], } )


    net = {"nodes" : nodes,
           "links" : links }


    return json.dumps( net )

