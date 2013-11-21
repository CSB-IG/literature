#!/usr/bin/env python
import os
import sys
import pprint
import argparse


parser = argparse.ArgumentParser(description='Construct meshterm network for search criteria.')
parser.add_argument('--outfile', type=argparse.FileType('w'), required=True,
                    default=sys.stdout)
parser.add_argument('--year', nargs='?', default=None, type=int, required=True)


if __name__ == '__main__':
      os.environ['DJANGO_SETTINGS_MODULE'] = "meddle.settings"
      sys.path.append('/home/rgarcia/caopsci/meddle/')

      execfile('/home/rgarcia/caopsci/dcaopsci_env/bin/activate_this.py',
               dict(__file__='/home/rgarcia/caopsci/dcaopsci_env/bin/activate_this.py'))

      from medline.network import mesh_network
      from medline.models import Citation
      import pickle

      args    = parser.parse_args()
      outfile = args.outfile

      G = mesh_network( Citation.objects.filter( date_created__year = args.year ) ) 

      print "nodes: ", len(G.nodes())
      
    
      pickle.dump(G, outfile)
      outfile.close()
