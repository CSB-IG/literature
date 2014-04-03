from django.core.management.base import BaseCommand, CommandError

from medline.models import *

from Bio import Medline
import time, datetime

class Command(BaseCommand):
    args = '</path/to/medline.txt>'
    help = 'loads citations from medline file'

    def handle(self, *args, **options):
        for path in args:

            records = Medline.parse( open(path) )
            for r in records:
                try:
                    cit = Citation()
                    cit.pmid                  = int(r['PMID'])

                    cit.title = r['TI'] if 'TI' in r.keys() else None
                    cit.abstract = r['AB'] if 'AB' in r.keys() else None
                    cit.pagination = r['PG'] if 'PG' in r.keys() else None
                    cit.copyright_information = " ; ".join(r['CI']) if 'CI' in r.keys() else None

                    # dates
                    if 'CRDT' in r.keys():
                        conv = time.strptime( r['CRDT'][0], "%Y/%m/%d %H:%M" )
                        cit.date_created          = datetime.datetime(*conv[:6])
                    if 'DCOM' in r.keys():
                        # 'DCOM': '19990406'
                        conv = time.strptime( r['DCOM'], "%Y%m%d" )
                        cit.date_completed        = datetime.datetime(*conv[:6])
                    if 'LR' in r.keys():
                        conv = time.strptime( r['LR'], "%Y%m%d" )
                        cit.date_revised          = datetime.datetime(*conv[:6])
                    if 'DEP' in r.keys():
                        conv = time.strptime( r['DEP'], "%Y%m%d" )
                        cit.date_electronic_publication = datetime.datetime(*conv[:6])

                    cit.save()

                    # relationships 
                    
                    # type
                    if 'PT' in r.keys():
                        for pub_type in r['PT']:
                            (pt, created) = PubType.objects.get_or_create(pub_type=pub_type)
                            cit.pub_types.add( pt )

                    # authors
                    if 'AU' in r.keys():
                        for i, author in enumerate(r['AU']):
                            if author !=  'et al.':
                                (a, created) = Author.objects.get_or_create(name = author,
                                                         full_name = r['FAU'][i])
                                cit.authors.add( a )

                    # language
                    if 'LA' in r.keys():
                        for lang in r['LA']:
                            (l, created) = Language.objects.get_or_create( language = lang )
                            cit.languages.add( l )


                    # affiliation
                    if 'AD' in r.keys():
                        (organization, created) = Organization.objects.get_or_create(name = r['AD'])
                        cit.affiliation = organization


                    # journal
                    if 'JID' in r.keys():
                        issn   = r['IS'] if 'IS' in r.keys() else None
                        volume = r['VI'] if 'VI' in r.keys() else None
                        issue  = r['IP'] if 'IP' in r.keys() else None

                        (journal, created) = Journal.objects.get_or_create(jid              = r['JID'],
                                                        issn             = issn,
                                                        volume           = volume,
                                                        issue            = issue,
                                                        title            = r['JT'],
                                                        iso_abbreviation = r['TA'],
                                                        country          = r['PL'] )
                        cit.journal = journal



                    cit.save()
                    
                    # meshterms
                    for term in r['MH']:
                        term_subs = term.split('/')
                        if term_subs[0].startswith('*'):
                            (mh, created) = Meshterm.objects.get_or_create(term=term_subs[0][1:])
                            major = True
                        else:
                            (mh, created) = Meshterm.objects.get_or_create(term=term_subs[0])
                            major = False
                
                        mc = Meshcitation.objects.create( meshterm = mh,
                                                          citation = cit, 
                                                          major    = major)
            

                        if len(term_subs) > 1:
                            for subterm in term_subs[1:]:
                                if subterm.startswith('*'):
                                    major = True
                                    subterm = subterm[1:]
                                else:
                                    major = False
                        
                                (sh, created) = Subheading.objects.get_or_create( term = subterm )
                                sht = Subheadingterm.objects.create( subheading   = sh,
                                                                     meshcitation = mc,
                                                                     major        = major )

                    self.stdout.write('%s' % cit)

                except:
                    print "error trying to load %s" % r['PMID']
                    import pprint
                    import sys
                    print sys.exc_info()[0]
                    pprint.pprint(r)
                    raise
