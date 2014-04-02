from medline import *

from Bio import Medline, Entrez
import time, datetime

Entrez.email = 'jsiqueiros@inmegen.gob.mx'

args = ['"tabernaemontana"[MeSH Terms]']

connect('medline')

for term in args:
    print "buscando [%s]" % term
    handle = Entrez.esearch( db="pubmed", retmax=10, term=term ) 
    record = Entrez.read(handle)

    ids_list = record['IdList']

    for id in ids_list:
        a = Entrez.efetch( db="pubmed", id=id, rettype='medline', retmode='text' )
        ff = a.readlines()
        records = Medline.parse(ff)
        r = records.next()


        cit = Citation()
        cit.pmid                  = int(r['PMID'])
        cit.title = r['TI'] if 'TI' in r.keys() else None
        cit.abstract = r['AB'] if 'AB' in r.keys() else None

        # dates
        if 'CRDT' in r.keys():
            conv = time.strptime( r['CRDT'][0], "%Y/%m/%d %H:%M" )
            cit.date_created = datetime.datetime(*conv[:6])
        if 'DCOM' in r.keys():
            # 'DCOM': '19990406'
            conv = time.strptime( r['DCOM'], "%Y%m%d" )
            cit.date_completed = datetime.datetime(*conv[:6])
        if 'LR' in r.keys():
            conv = time.strptime( r['LR'], "%Y%m%d" )
            cit.date_revised = datetime.datetime(*conv[:6])
        if 'DEP' in r.keys():
            conv = time.strptime( r['DEP'], "%Y%m%d" )
            cit.date_electronic_publication = datetime.datetime(*conv[:6])

        # type
        if 'PT' in r.keys():
            cit.pub_types = r['PT']

        # authors
        if 'AU' in r.keys():
            authors = []
            for i,author in enumerate(r['AU']):
                if author != 'et al.':
                    authors.append(r['FAU'][i])
            cit.authors = authors
                                    

        # language
        if 'LA' in r.keys():
            for lang in r['LA']:
                cit.languages = r['LA']


        # affiliation
        if 'AD' in r.keys():
            cit.affiliation = r['AD']

        # meshterms
        if 'MH' in r:
            cit.meshterms = r['MH']


        cit.save()
