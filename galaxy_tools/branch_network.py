#!/usr/bin/env python
import os
import sys
import pprint
import argparse
import json


parser = argparse.ArgumentParser(description='Construct branch network for given year.')
parser.add_argument('--outfile', type=argparse.FileType('w'), required=True,
                    default=sys.stdout)
parser.add_argument('--year', nargs='?', default=None, type=int)

parser.add_argument('--root1', type=str, required=True)
parser.add_argument('--root2', type=str, required=True)
parser.add_argument('--root3', type=str, required=True)






if __name__ == '__main__':
      os.environ['DJANGO_SETTINGS_MODULE'] = "meddle.settings"
      sys.path.append('/home/rgarcia/caopsci/meddle/')

      execfile('/home/rgarcia/caopsci/dcaopsci_env/bin/activate_this.py',
               dict(__file__='/home/rgarcia/caopsci/dcaopsci_env/bin/activate_this.py'))
      from medline.network import *

      args    = parser.parse_args()
      outfile = args.outfile
      year    = args.year

      G = branch_network( year, (args.root1,
                                 args.root2,
                                 args.root3) )


      print "year:", year
      print "roots:", args.root1, args.root2, args.root3
      
      outfile.write( json.dumps(branch_network2hive(G),
                                indent=4))
