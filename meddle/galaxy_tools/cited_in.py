#!/usr/bin/env python

execfile('/home/rgarcia/caopsci/dcaopsci_env/bin/activate_this.py',
         dict(__file__='/home/rgarcia/caopsci/dcaopsci_env/bin/activate_this.py'))

import os
import sys

if __name__ == '__main__':
      os.environ['DJANGO_SETTINGS_MODULE'] = "meddle.settings"
      sys.path.append('/home/rgarcia/caopsci/meddle/')


from medline.network import *


import pprint

if __name__ == '__main__':

      outfile = open ( sys.argv[1], 'w')
      terms   = sys.argv[2].strip().split('__cr____cn__')

      
      pprint.pprint(terms)

      outfile.write( json.dumps(cited_in_network( terms ),
                                indent=4))
