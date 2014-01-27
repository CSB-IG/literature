# loads sqlite database from medline.txt file

from elixir import *
from models.medline import *
import time, datetime
import pprint
from sqlalchemy.exc import IntegrityError
import sys

# metadata.bind = 'mysql+oursql://caopsci:G@localhost/medline'
metadata.bind = 'sqlite:////home/jmsiqueiros/caopsci/trending_topics/Data/medline.sqlite'

setup_all()
create_all()





from elixir import Entity

def get_by_or_init(cls, if_new_set={}, **params):
	"""Call get_by; if no object is returned, initialize an
	object with the same parameters.  If a new object was
	created, set any initial values."""
	
	result = cls.get_by(**params)
	if not result:
		result = cls(**params)
		result.set(**if_new_set)
	return result

Entity.get_by_or_init = classmethod(get_by_or_init)







#
# abrimos archivo plano
#
medline_input = sys.argv[1]

from Bio import Medline

records = Medline.parse( open(medline_input) )
for r in records:
    try:
        cit = Citation()
        cit.pmid                  = r['PMID']

        if 'TI' in r.keys():
            cit.article_title         = r['TI'] 
        if 'AB' in r.keys():
            cit.abstract              = r['AB'] 
        if 'PG' in r.keys():
            cit.pagination            = r['PG'] 
        if 'CI' in r.keys():
            cit.copyright_information = " ; ".join(r['CI'])

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


        # relationships 

        # type
        if 'PT' in r.keys():
            for pub_type in r['PT']:
                pt = PubType.get_by_or_init(pub_type=pub_type)
                cit.pub_types.append( pt )

        # authors
        if 'AU' in r.keys():
            for i, author in enumerate(r['AU']):
                if author !=  'et al.':
                    a = Author.get_by_or_init(name      = author,
                                              full_name = r['FAU'][i])
                    cit.authors.append( a )

        # language
        if 'LA' in r.keys():
            for lang in r['LA']:
                l = Language.get_by_or_init(language= lang )
                cit.languages.append( l )


        # affiliation
        if 'AD' in r.keys():
            organization    = Organization.get_by_or_init(name = r['AD'])
            cit.affiliation = organization


        # journal
        if 'JID' in r.keys():
            issn = r['IS'] if 'IS' in r.keys() else None
            
            if 'VI' in r.keys():
                volume = r['VI']
            else:
                volume = None
            if 'IP' in r.keys():
                issue      = r['IP']
            else:
                issue = None

            journal = Journal.get_by_or_init(jid              = r['JID'],
                                             issn             = issn,
                                             volume           = volume,
                                             issue            = issue,
                                             title            = r['JT'],
                                             iso_abbreviation = r['TA'],
                                             country          = r['PL'] )
            cit.journal = journal


        # meshterms
        for term in r['MH']:
            term_subs = term.split('/')
            if term_subs[0].startswith('*'):
                mh = Meshterm.get_by(term=term_subs[0][1:])
                major = True
            else:
                mh = Meshterm.get_by(term=term_subs[0])
                major = False
                
            tc          = TermCitation()
            tc.term     = mh
            tc.major    = major
            tc.citation = cit
            tc.merge()
            
            session.commit()

            if len(term_subs) > 1:
                for subterm in term_subs[1:]:
                    if subterm.startswith('*'):
                        major = True
                        subterm = subterm[1:]
                    else:
                        major = False
                        
                    sh = Subheading.get_by_or_init( sh = subterm )
                    sht = SubheadingTerm( sh           = sh,
                                          termcitation = tc,
                                          major        = major )
                    sht.merge()
                    tc.subheadings.append(sht)
                session.commit()
                
            cit.meshterms.append(tc)

        session.commit()
        print cit
    except IntegrityError as e:
        print "error trying to load %s" % r['PMID']
        pprint.pprint(e)
        pprint.pprint(r)
        session.rollback()
        
