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

            citation = Citation()
            for l in lineas:
                try:
                    (pmid, citedin) = l.split(',')

                    if pmid != citation.pmid:
                        citation = Citation.objects.get(pmid=pmid)
        
                    cited_in = Citation.objects.get(pmid=citedin)
                    if cited_in:
                        citation.cited_in.add( cited_in )
                        print "%s cited in %s" % (citation.pmid, cited_in.pmid)
            
                except:
                    pass

