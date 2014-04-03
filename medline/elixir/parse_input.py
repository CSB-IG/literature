##Busca los mesh terms en un archivo local y genera la red mesh term-PMID-mesh term
from Bio import Medline
import pprint
input = open("/home/rgarcia/medline/00.txt")
records = Medline.parse(input)
for record in records:
	for term_a in record['MH']:
		for term_b in record['MH']:
			print "%s|%s|%s|%s" % (record['DP'], term_a.replace(' ','_'), record['PMID'], term_b.replace(' ','_'))

			
