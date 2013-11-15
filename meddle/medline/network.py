from django.db.models import Q
from medline.models import *
from random import shuffle
import json, itertools, datetime
import networkx as nx
import pprint

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


def meshset_network( year ):
    citations = Citation.objects.filter( date_created__year = year )

    G = nx.Graph()

    for cit in citations.all():
        keys = []
        for msh in cit.meshcitation_set.all():
            keys.append(msh)

        for pair in itertools.combinations( keys, 2 ):
            source = pair[0]
            target = pair[1]
                
            j = float(len(source.mesh_set().intersection(target.mesh_set()))) / float(len(source.mesh_set().union(target.mesh_set())))

            e = G.get_edge_data(source.majorless(), target.majorless())

            if not e:
                G.add_edge(source.majorless(), target.majorless(), weight=1, j=j)
            else:
                G.add_edge(source.majorless(), target.majorless(), weight=e['weight']+1, j=j)
    #print G                
    return G



# def jaccard_index( year ):
#     citations = Citation.objects.filter( date_created__year = year )

#     G = nx.Graph()
#     terms = []
#     for cit in citations.all():
#         for msh in cit.meshcitation_set.all():
#             terms.append(msh)

#     jaccards = []
#     for pair in itertools.combinations( terms, 2 ):
#         source = pair[0]
#         target = pair[1]

#         j = float(len(source.mesh_set().intersection(target.mesh_set()))) / float(len(source.mesh_set().union(target.mesh_set())))
#         jaccards.append(j)

    # TODO: devolver promedio

# def jaccard_distance( year): A desarrollar




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



# computes jacard index for two sets
def jaccard_index( a, b):
    return float(len(a.intersection(b))) / float(len(a.union(b)))


def jaccard_index_multi(first, *others):
    return float( len( first.intersection(*others))) / float(len(first.union(*others)))


def mesh_pmid_matrix( year ):
    citations = Citation.objects.filter( date_created__year = year )
    with open('/home/jmsiqueiros/Escritorio/test.txt', 'w') as f:
        for cit in citations.all():
            for n in cit.bow_jin():
                f.write("%s|%s|%s\n" % (n[0], cit.pmid, n[1]) )




def mesh_jin_network( year ):
    citations = Citation.objects.filter( date_created__year = year )

    G = nx.Graph()
    
    for cit in citations.all():
        for pair in itertools.combinations( cit.bow_jin(), 2 ):
            source = pair[0]
            target = pair[1]
            
            e = G.get_edge_data(source[0], target[0])

            if not e:
                G.add_edge(source[0], target[0], weight=( source[1] + target[1] )/2.0 )
            else:
                G.add_edge(source[0], target[0], weight=e['weight'] + ( source[1] + target[1] )/2.0 )

        
    return G



def mesh_network( year ):
    citations = Citation.objects.filter( date_created__year = year )

    G = nx.Graph()

    for cit in citations.all():
        keys = []
        for msh in cit.meshcitation_set.all():
            keys.append(msh)

        for pair in itertools.combinations( keys, 2 ):
            source = pair[0]
            target = pair[1]
                
            e = G.get_edge_data(source.majorless(), target.majorless())

            if not e:
                G.add_edge(source.majorless(), target.majorless(), weight=1)
            else:
                G.add_edge(source.majorless(), target.majorless(), weight=e['weight']+1)

    return G



def mesh_jin_weighted_network( year ):
    citations = Citation.objects.filter( date_created__year = year )

    G = nx.Graph()

    for cit in citations.all():
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
        v = G.get_edge_data(*e)
        if len(v['citations'])>1:
            print e,G.get_edge_data(*e)
            sets = []
            for cit in v['citations']:
                sets.append(cit.bag_of_words())

            H.add_edge(e[0], e[1], weight=jaccard_index_multi( *sets ))


    return H
