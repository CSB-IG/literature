import sys
from Bio import Medline
from pymongo import MongoClient
import time, datetime

client  = MongoClient()
db      = client.literature
medline = db.medline


medline_input = sys.argv[1]

records = Medline.parse( open(medline_input) )
for r in records:

    # evenly format dates
    if 'CRDT' in r.keys():
        conv = time.strptime( r['CRDT'][0], "%Y/%m/%d %H:%M" )
        r['CRDT'] = datetime.datetime(*conv[:6]) # date created
    if 'DCOM' in r.keys():
        conv = time.strptime( r['DCOM'], "%Y%m%d" )
        r['DCOM'] = datetime.datetime(*conv[:6]) # date completed
    if 'LR' in r.keys():
        conv = time.strptime( r['LR'], "%Y%m%d" )
        r['LR'] = datetime.datetime(*conv[:6]) # date revised
    if 'DEP' in r.keys():
        conv = time.strptime( r['DEP'], "%Y%m%d" )
        r['DEP'] = datetime.datetime(*conv[:6]) # date of electronic publication

    medline.insert(r)
