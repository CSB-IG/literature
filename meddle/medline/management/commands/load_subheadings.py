from django.core.management.base import BaseCommand, CommandError

from medline.models import *

from Bio import Medline


class Command(BaseCommand):
    args = '</path/to/d2013.bin>'
    help = 'loads subheadings from bin file'

    def handle(self, *args, **options):
        for path in args:

            #
            # cargamos subheadings
            #
            f = open(path, 'r')
            lines = f.readlines()
            f.close()
            for l in lines:
                if l.startswith('MH ='):
                    (tag, mh) = l.split(' = ')
                    sh = Subheading.objects.create( term = mh.rstrip() )
                    self.stdout.write('%s' % sh)

