from django.core.management.base import BaseCommand, CommandError

from medline.models import *

from Bio import Medline


class Command(BaseCommand):
    args = '</path/to/meshterms.txt>'
    help = 'loads mesterms from meshterms file'

    def handle(self, *args, **options):
        for path in args:


            f =open(path, 'r')
            lineas = f.readlines()
            f.close()

            for l in lineas:
                if l.startswith('MH ='):
                    (tag, mh) = l.split(' = ')
                    msh = Meshterm.objects.create(
                        term = mh.rstrip() )
                    self.stdout.write('%s' % msh)

