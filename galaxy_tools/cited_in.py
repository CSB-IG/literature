#!/usr/bin/env python
import os
import sys
import pprint
import argparse
import json


parser = argparse.ArgumentParser(description='Construct citation network from search criteria.')
parser.add_argument('--outfile', type=argparse.FileType('w'), required=True,
                    default=sys.stdout)

parser.add_argument('--start_year', nargs='?', default=None, type=int)
parser.add_argument('--end_year', nargs='?', default=None, type=int)

parser.add_argument('--terms', type=str, nargs='*',
                    help='one or more search terms')




if __name__ == '__main__':
      os.environ['DJANGO_SETTINGS_MODULE'] = "meddle.settings"
      sys.path.append('/home/rgarcia/caopsci/meddle/')

      execfile('/home/rgarcia/caopsci/dcaopsci_env/bin/activate_this.py',
               dict(__file__='/home/rgarcia/caopsci/dcaopsci_env/bin/activate_this.py'))
      from medline.network import cited_in_network, citation_network2dict

      args    = parser.parse_args()
      outfile = args.outfile
      terms   = args.terms
      # terms   = sys.argv[2].strip().split('__cr____cn__')

      print "terms: "
      pprint.pprint(terms)

      G = cited_in_network( terms ) 

      print "nodes: ", len(G.nodes())
      
    
      pickle.dump(G, output)
      output.close()
