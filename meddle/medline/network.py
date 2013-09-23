from django.db.models import Q
from medline.models import *
from random import shuffle
import json, itertools, datetime
import networkx as nx


# format network as json
def citation_network2json(G):
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
        q_ob |= Q(meshterms__term__contains=term)
    
    citations = Citation.objects.filter(q_ob)

    print len(citations)
    
    G = nx.DiGraph()

    for cited in citations:
        # create network from citedin links
        for citer in cited.cited_in.all():
            if len(set(citer.major_terms()).intersection(set(cited.major_terms())))>0:
                G.add_edge( citer,
                            cited,
                            weight = len(set(cited.meshterms.all()).intersection(set(citer.meshterms.all()))))

    print len(G.nodes())
    return citation_network2json( G )
