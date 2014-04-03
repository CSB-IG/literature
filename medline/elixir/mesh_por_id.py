##Busqueda de Mesh terms por id del articulo y genera la red

from Bio import Entrez
from Bio import Medline
import pprint

IDs = [
       '23087226'
       ]

Entrez.email = 'jsiqueiros@inmegen.gob.mx'

for ID in IDs:

    # configuramos busqueda del articulo por ID

    handle = Entrez.efetch(db= 'pubmed', id= ID,  rettype = 'medline', retmode = 'text')

records = Medline.parse(handle)

#for record in records:
	#print record['MH']
    # el resultado es una lista de articulos
for record in records:
	for term_a in record['MH']:
		for term_b in record['MH']:
			print "%s %s %s" % (term_a.replace(' ','_'), ID, term_b.replace(' ','_'))
