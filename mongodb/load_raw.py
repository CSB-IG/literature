import argparse
from Bio import Medline
from pymongo import MongoClient
import time, datetime

parser = argparse.ArgumentParser(description='Load citations from Medline file to MongoDB.')
parser.add_argument('--citations', type=argparse.FileType('r'), required=True)

args    = parser.parse_args()

client  = MongoClient()
db      = client.literature
medline = db.medline

records = Medline.parse( args.citations )
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


    # let PubMed handle keys
    r['_id'] = int(r['PMID'])
    
    medline.save(r)
