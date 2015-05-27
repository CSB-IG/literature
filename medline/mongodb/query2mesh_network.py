#!/usr/bin/env python
import os
import sys
import pprint
import argparse
from network import mesh_network
from article_network import article_network
import pickle
from pymongo import MongoClient
import json

client  = MongoClient()
db      = client.literature
medline = db.medline



parser = argparse.ArgumentParser(description='Construct meshterm network for search criteria.')
parser.add_argument('--query', type=str, required=True)
parser.add_argument('--outfile', type=argparse.FileType('wb'), required=True,
                    default=sys.stdout)
parser.add_argument('--type', type=str, required=False)

if __name__ == '__main__':

      args    = parser.parse_args()
      outfile = args.outfile
      type = args.type
      
      print unicode(args.query)
      
      if args.type:
      	if type=="article":
              G = article_network( medline.find( json.loads(args.query) ) )
        else:
          G = mesh_network( medline.find( json.loads(args.query) ) )
      else:
      	G = mesh_network( medline.find( json.loads(args.query) ) )

      print "nodes: ", len(G.nodes())
    
      pickle.dump(G, outfile)
      outfile.close()
