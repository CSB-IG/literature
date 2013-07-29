from django.core.management.base import BaseCommand, CommandError

from medline.models import *

from Bio import Medline


class Command(BaseCommand):
    args = '</path/to/mtrees.bin>'
    help = 'loads branches from bin file'

    def handle(self, *args, **options):
        for path in args:


            #
            # cargamos el diccionario de branches
            #
            f = open(path, 'r')
            lines = f.readlines()
            f.close()
            for line in lines:
                (term, branch) = line.split(';')
                (mh, created) = Meshterm.objects.get_or_create(term=term.rstrip())

                br = Branch.objects.create(branch=branch.rstrip(), term=mh)

                self.stdout.write('%s' % br)

