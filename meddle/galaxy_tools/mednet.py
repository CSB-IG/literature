#!/usr/bin/env python

execfile('/home/rgarcia/caopsci/dcaopsci_env/bin/activate_this.py',
         dict(__file__='/home/rgarcia/caopsci/dcaopsci_env/bin/activate_this.py'))

import os
import sys

if __name__ == '__main__':

      # Setup environ
      os.environ['DJANGO_SETTINGS_MODULE'] = "meddle.settings"
      sys.path.append('/home/rgarcia/caopsci/meddle/')


from medline.models import *
from random import shuffle
import json, itertools, datetime
import networkx as nx

import pprint



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


def cited_in( year ):
    citations = Citation.objects.filter( date_created__year=year)

    G = nx.DiGraph()
    # create network from citedin links
    for cited in citations:
        for citer in cited.cited_in.all():
            G.add_edge(cited, citer)

    return G
    #pprint.pprint( citation_network2json(G) )



if __name__ == '__main__':
      outfile = open ( sys.argv[1], 'w')
      outfile.write( json.dumps(citation_network2json(cited_in(1991)),
                                indent=4))
