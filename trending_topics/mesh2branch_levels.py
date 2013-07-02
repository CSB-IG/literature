from elixir import *
from models.medline import *
import time, datetime
import pprint
import networkx as nx
import numpy
import itertools

metadata.bind = 'mysql+oursql://caopsci:G@localhost/medline'

setup_all()


level = 3


for year in range(1987,2014):
    start = datetime.datetime(year,1,1)
    end   = datetime.datetime(year+1,1,1)

    year_query = Citation.query.filter(Citation.date_created>=start,
                                       Citation.date_created<=end)
    G = nx.Graph()

    for cit in year_query.all():
        msh_branch = {}
        try:
            for msh in cit.meshterms:
                for branch in msh.term.branches:
                    leaves = branch.branch.split('.')
                    if len(leaves) >= level:
                        truncated = '.'.join( leaves[0:level] )
                        msh_branch[msh.term] = truncated



            for pair in itertools.combinations( cit.meshterms, 2 ):
                key_s = msh_branch[pair[0].term]
                key_t = msh_branch[pair[1].term]
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
    
    with open('branch_nx_l'+str(level)+'_'+str(year)+'.csv', 'w') as f:
        for e in G.edges():
            z = ( float(G.get_edge_data(e[0], e[1])['weight']) /arr.max()) * 100
            f.write("%s,%s,%s\n" % (e[0], e[1], z))
