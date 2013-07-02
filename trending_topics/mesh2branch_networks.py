from elixir import *
from models.medline import *
import time, datetime
import pprint
import networkx as nx
import numpy

metadata.bind = 'mysql+oursql://caopsci:G@localhost/medline'

setup_all()





for year in range(1987,2014):
    start = datetime.datetime(year,1,1)
    end   = datetime.datetime(year+1,1,1)

    year_query = Citation.query.filter(Citation.date_created>=start,
                                       Citation.date_created<=end)
    G = nx.Graph()

    for cit in year_query.all():
        try:
            for mh_source in cit.meshterms:
                for mh_target in cit.meshterms:
                    for branch_s in mh_source.term.branches:
                        key_s = branch_s.branch[:1]
                        for branch_t in mh_target.term.branches:
                            key_t = branch_t.branch[:1]
                            if key_s != key_t:
                                e = G.get_edge_data(key_s, key_t)
                                if not e:
                                    G.add_edge(key_s, key_t, weight=1)
                                else:
                                    G.add_edge(key_s, key_t, weight=e['weight']+1)
                                
        except:
            pass


    weights = []
    for e in G.edges():
        weights.append(float(G.get_edge_data(e[0], e[1])['weight']))

    arr = numpy.array(weights)
    arr /= 2.0
    
    with open('branch_network_'+str(year)+'.csv', 'w') as f:
        for e in G.edges():
            x = int( G.get_edge_data(e[0], e[1])['weight'] ) /2
            z = (x/arr.max()) * 100
            f.write("%s,%s,%s\n" % (e[0], e[1], z))
