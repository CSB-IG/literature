import argparse
from Bio import Entrez
from Bio import Medline
from pprint import pprint
 #Con argparse definir desde consola la variable terms con los criterios de busqueda deseados.

Entrez.email = "jmario.siqueiros@iimas.unam.mx"

terms = 'genomics[MESH] AND individualized medicine[TIAB] OR genomics[MESH] AND personalized medicine[ALL]'

pmids = Entrez.read( Entrez.esearch ( db='pubmed', term=terms, retmax= '10' ) )['IdList']

for pmid in pmids:
    handle = Entrez.efetch( db = 'pubmed',
                            id = pmid,
                            rettype = 'medline',
                            retmode = 'text')

    records = Medline.parse(handle)
    
    for record in records:
        for mesh_o in record['MH']:
            for mesh_d in record['MH']:
                 print "%s %s %s" % (mesh_o.replace(' ','_'),'|',mesh_d.replace(' ','_'))
