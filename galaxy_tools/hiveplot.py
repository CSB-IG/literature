#!/usr/bin/env python
# coding: utf8

execfile('/home/rgarcia/caopsci/dcaopsci_env/bin/activate_this.py',
         dict(__file__='/home/rgarcia/caopsci/dcaopsci_env/bin/activate_this.py'))

import os
import sys

from django.template.loader import render_to_string

if __name__ == '__main__':
      # Setup environ
      os.environ['DJANGO_SETTINGS_MODULE'] = "meddle.settings"
      sys.path.append('/home/rgarcia/caopsci/meddle/')

      print sys.argv[1]
      inputfile = open ( sys.argv[1], 'r')
      net = inputfile.read()
      inputfile.close()
      
      outfile = open ( sys.argv[2], 'w')
      outfile.write(
            render_to_string('medline/hiveplot.html', {'net': net}) )
