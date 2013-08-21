from django.http import HttpResponse
from medline.models import *
from random import shuffle
import json, itertools, datetime
import networkx as nx

import pprint

def cited_in(request, year):
    citations = Citation.objects.filter( date_created__year=year)

    G = nx.DiGraph()
    # create network from citedin links
    for cited in citations:
        for citer in cited.cited_in.all():
            G.add_edge(cited.pmid, citer.pmid)
    
    return HttpResponse( json.dumps(G.edges()),
                         mimetype='application/json' )                         




def cited_in_trends(request, year):
    G = nx.DiGraph()
    for sh in Subheadingterm.objects.filter(subheading = Subheading.objects.filter(term='Trends'),
                                            major=True,
                                            meshcitation__citation__date_created__gte=datetime.datetime(int(year),1,1)):
        cited = sh.meshcitation.citation
        # create network from citedin links
        for citer in cited.cited_in.all():
            if len(set(citer.major_terms()).intersection(set(cited.major_terms())))>0:
                G.add_edge( citer,
                            cited,
                            weight = len(set(cited.meshterms.all()).intersection(set(citer.meshterms.all()))))
    

    # format network as json
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
                       "target": nodei.index(e[1]),
                       "weight" : G.get_edge_data(*e)['weight']} )

    net = {"nodes" : nodes,
           "links" : links }


    return HttpResponse( json.dumps(net, indent=4),
                         mimetype='application/json' )                         







def mesh_network(request, year_start, year_end):
    citations = Citation.objects.filter( date_created__gte = datetime.datetime(int(year_start), 01, 01),
                                         date_created__lt  = datetime.datetime(int(year_end) + 1, 01,01))

    G = nx.Graph()

    for cit in citations.all():
        for pair in itertools.combinations( cit.meshterms.all(), 2 ):
            mh_source = pair[0]
            mh_target = pair[1]
            e = G.get_edge_data(mh_source, mh_target)
            if not e:
                G.add_edge(mh_source, mh_target, weight=1, year=cit.date_created.year)
            else:
                G.add_edge(mh_source, mh_target, weight=e['weight']+1, year=cit.date_created.year)
                    





    raw_nodes = G.nodes()
    nodes = []
    for i,node in enumerate(raw_nodes):
        roots = []
        for branch in node.branch_set.all():
            roots.append(branch.branch[:1])
        if roots:
            shuffle(roots)
            group = roots.pop()
        else:
            group = 0
        nodes.append( {"name": "%s" % node.term,
                       "group": group,
                       "degree": G.degree(node) } )


    links = []
    for e in G.edges():
        links.append( {"source": raw_nodes.index(e[0]),
                       "target": raw_nodes.index(e[1]),
                       "year": G.get_edge_data(e[0], e[1])['year'],
                       "value" : float(G.get_edge_data(e[0], e[1])['weight'])} )

    net = {"nodes" : nodes,
           "links" : links }
    return HttpResponse( json.dumps( net ),
                         mimetype='application/json' )







def branch_network(request, year):
    citations = Citation.objects.filter( date_created__year = year )

    G = nx.Graph()

    for cit in citations.all():
        keys = []
        for msh in cit.meshterms.all():
            for branch in msh.branch_set.all():
                keys.append( ".".join(branch.branch.split('.')[:3]) )


        for pair in itertools.combinations( keys, 2 ):
            source = pair[0]
            target = pair[1]
                
            e = G.get_edge_data(source, target)
            if not e:
                G.add_edge(source, target, weight=1)
            else:
                G.add_edge(source, target, weight=e['weight']+1)
                    

    raw_nodes = G.nodes()
    nodes = []
    for i,node in enumerate(raw_nodes):
        group = node[:1]
        nodes.append( {"name": node,
                       "group": group,
                       "degree": G.degree(node) } )


    links = []
    for e in G.edges():
        links.append( {"source": raw_nodes.index(e[0]),
                       "target": raw_nodes.index(e[1]),
                       "value" : float(G.get_edge_data(e[0], e[1])['weight'])} )

    net = {"nodes" : nodes,
           "links" : links }
    return HttpResponse( json.dumps( net ),
                         mimetype='application/json' )
    
