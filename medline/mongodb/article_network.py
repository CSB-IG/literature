import itertools
import networkx as nx
import pprint
import sets

# computes jacard index for two or mor sets
def jaccard_index(first, *others):
    return float( len( first.intersection(*others))) / float(len(first.union(*others)))


def article_network( cursor ):

    G = nx.Graph()
    sets = [set() for i in range(cursor.count())]
    keys = []
    
    i=0
    for cit in cursor:
        G.add_node(cit['PMID'])
        sets[i]= cit['MH']
        keys.append(cit['PMID'])
        i=i+1;
        
        print(cit['PMID'])
        
    print(keys)
        
    for pair in itertools.combinations(range(0,cursor.count()),2):
        set0 = sets[pair[0]]
        set1 = sets[pair[1]]
        und = set(set0)&set(set1)
        print(str(len(und))+ "      "+str(keys[pair[0]])+"   "+str(keys[pair[1]]) )
        G.add_edge(keys[pair[0]], keys[pair[1]], terms = und, weight = len(und)  )
        
    return G
