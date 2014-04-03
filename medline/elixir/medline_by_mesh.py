#Trae id de los articulos que tienen el mesh term 'genomics'. para buscar articulos con otro mesh term, sustiuir el mesh por el termino de interes en term='meshterm['MH']

from Bio import Entrez
#import cPickle, bz2
import os

writer = open( 'medfile.txt', 'w' )

Entrez.email = 'jsiqueiros@inmegen.gob.mx'

handle = ( Entrez.esearch( db="pubmed", retmax=10, term='genomics[MH]' ) )
record = Entrez.read(handle)

ids_list = record['IdList']

mdl_records = ( Entrez.efetch( db="pubmed", id=ids_list, rettype='medline', retmode='text' ) )

writer.write(mdl_records.read())

writer.close()

#print(mdl_records.read())


#Falta buscar la manera para que haga una busqueda cada x tiempo y no repita registros. Tambien falta encotrar el metodo para cargar los resultados en la base de datos.
