from django.http import HttpResponse
from django.shortcuts import render_to_response
from medline.models import *
from random import shuffle
import json, itertools, datetime
import networkx as nx
import csv
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

    # indent=4 for pretty printing
    return HttpResponse( json.dumps(net), 
                         mimetype='application/json' )                         


def jurisprudence_network(request):

    for year in range(1987,2014):
        G = nx.Graph()

        jurisprudence = Meshterm.objects.filter(term="Jurisprudence")[0]

        for cit in jurisprudence.citation_set.filter(date_created__year=year):
            for pair in itertools.combinations( cit.meshcitation_set.all(), 2 ):
                e = G.get_edge_data(*pair)
                if not e:
                    G.add_edge(*pair, weight=1 )
                else:
                    G.add_edge(*pair, weight=e['weight']+1 )
    
    
        letj = Subheading.objects.filter(term="legislation & jurisprudence")[0]
        for sh in letj.subheadingterm_set.all():
            cit = sh.meshcitation.citation
            if cit.date_created.year == year:
                for pair in itertools.combinations( cit.meshcitation_set.all(), 2 ):
                    e = G.get_edge_data(*pair)
                    if not e:
                        G.add_edge(*pair, weight=1 )
                    else:
                        G.add_edge(*pair, weight=e['weight']+1 )



        with open(str(year)+'_jurisprudence.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter='|')
            for pair in G.edges():
                weight = G.get_edge_data(*pair)['weight']
                csvwriter.writerow( [pair[0].__unicode__(), pair[1].__unicode__(), weight] )


def breast_cancer_network(request):

    for year in range(1987,2014):
        G = nx.Graph()

        breast_cancer = Meshterm.objects.filter(term="Breast Neoplasms")[0]

        for cit in breast_cancer.citation_set.filter(date_created__year=year):
            for pair in itertools.combinations( cit.meshcitation_set.all(), 2 ):
                e = G.get_edge_data(*pair)
                if not e:
                    G.add_edge(*pair, weight=1 )
                else:
                    G.add_edge(*pair, weight=e['weight']+1 )

        with open(str(year)+'_breast_cancer.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter='|')
            for pair in G.edges():
                weight = G.get_edge_data(*pair)['weight']
                csvwriter.writerow( [pair[0].__unicode__(), pair[1].__unicode__(), weight] )



def clinical_network(request):

    for year in range(1987,2014):
        G = nx.Graph()

        Clinical = Meshterm.objects.filter(term="Clinical Trial")[0]

        for cit in Clinical.citation_set.filter(date_created__year=year):
            for pair in itertools.combinations( cit.meshcitation_set.all(), 2 ):
                e = G.get_edge_data(*pair)
                if not e:
                    G.add_edge(*pair, weight=1 )
                else:
                    G.add_edge(*pair, weight=e['weight']+1 )
    
    
        clinical = Subheading.objects.filter(term="clinical")[0]
        for sh in clinical.subheadingterm_set.all():
            cit = sh.meshcitation.citation
            if cit.date_created.year == year:
                for pair in itertools.combinations( cit.meshcitation_set.all(), 2 ):
                    e = G.get_edge_data(*pair)
                    if not e:
                        G.add_edge(*pair, weight=1 )
                    else:
                        G.add_edge(*pair, weight=e['weight']+1 )



        with open(str(year)+'_clinical.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter='|')
            for pair in G.edges():
                weight = G.get_edge_data(*pair)['weight']
                csvwriter.writerow( [pair[0].__unicode__(), pair[1].__unicode__(), weight] )






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
                       "target": nodei.index(e[1]),
                       "weight" : G.get_edge_data(*e)['weight']} )

    net = {"nodes" : nodes,
           "links" : links }
    
    return net


def citation_list(request):
    # pprint.pprint(request.GET.getlist('meshterms'))
    f = CitationFilter(request.GET, queryset=Citation.objects.filter(date_created__lt=datetime.datetime(1990,1,1)))
    print len(f.qs)

    G = nx.DiGraph()

    for cited in f.qs:
        # create network from citedin links
        for citer in cited.cited_in.all():
            if len(set(citer.major_terms()).intersection(set(cited.major_terms())))>0:
                G.add_edge( citer,
                            cited,
                            weight = len(set(cited.meshterms.all()).intersection(set(citer.meshterms.all()))))

    print len(G.nodes())
    net = citation_network2json( G )

    # indent=4 for pretty printing
    return HttpResponse( json.dumps(net), 
                         mimetype='application/json' )                         


    
#    return render_to_response('medline/filter.html', {'filter': f})
