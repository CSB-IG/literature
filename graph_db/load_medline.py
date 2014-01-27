from medline import *
import time, datetime
import pprint
import sys

from bulbs.neo4jserver import Graph

g = Graph()
#nodes
g.add_proxy("citations", Citation)
g.add_proxy("authors", Author)
g.add_proxy("organizations", Organization)
g.add_proxy("meshterms", Meshterm)
g.add_proxy("journals", Journal)

# relationships
g.add_proxy("published_in", PublishedIn)
g.add_proxy("language", Language)
g.add_proxy("describes", Describes)


#
# abrimos archivo plano
#
medline_input = sys.argv[1]

from Bio import Medline

records = Medline.parse( open(medline_input) )
for r in records:
	cit = g.citations.create()
        cit.pmid                  = r['PMID']
	
        if 'TI' in r.keys():
		cit.article_title         = r['TI'] 
	if 'AB' in r.keys():
		cit.abstract              = r['AB'] 
	if 'PG' in r.keys():
		cit.pagination            = r['PG'] 
	if 'CI' in r.keys():
		cit.copyright_information = " ; ".join(r['CI'])
        if 'PT' in r.keys():
		cit.pub_type= r['PT'][0]

	cit.save()

        # authors
        if 'AU' in r.keys():
            for i, author in enumerate(r['AU']):
                if author !=  'et al.':
			a = g.authors.get_or_create(name      = author,
						    full_name = r['FAU'][i])
			published = g.published_in.create(cit, a)
			# dates
			if 'CRDT' in r.keys():
				conv = time.strptime( r['CRDT'][0], "%Y/%m/%d %H:%M" )
				published.date_created          = datetime.datetime(*conv[:6])
			if 'DCOM' in r.keys():
				# 'DCOM': '19990406'
				conv = time.strptime( r['DCOM'], "%Y%m%d" )
				published.date_completed        = datetime.datetime(*conv[:6])
			if 'LR' in r.keys():
				conv = time.strptime( r['LR'], "%Y%m%d" )
				published.date_revised          = datetime.datetime(*conv[:6])
			if 'DEP' in r.keys():
				conv = time.strptime( r['DEP'], "%Y%m%d" )
				published.date_electronic_publication = datetime.datetime(*conv[:6])

			published.save()

			# language
			if 'LA' in r.keys():
				for lang in r['LA']:
					l = g.language.create(cit, a)
					l.language = lang
					l.save()



        # affiliation
        if 'AD' in r.keys():
            organization    = g.organizations.get_or_create(name = r['AD'])
	    published = g.published_in.create(cit, organization)
	    # dates
	    if 'CRDT' in r.keys():
		    conv = time.strptime( r['CRDT'][0], "%Y/%m/%d %H:%M" )
		    published.date_created          = datetime.datetime(*conv[:6])
	    if 'DCOM' in r.keys():
		    # 'DCOM': '19990406'
		    conv = time.strptime( r['DCOM'], "%Y%m%d" )
		    published.date_completed        = datetime.datetime(*conv[:6])
	    if 'LR' in r.keys():
		    conv = time.strptime( r['LR'], "%Y%m%d" )
		    published.date_revised          = datetime.datetime(*conv[:6])
	    if 'DEP' in r.keys():
		    conv = time.strptime( r['DEP'], "%Y%m%d" )
		    published.date_electronic_publication = datetime.datetime(*conv[:6])

	    published.save()

	    # language
	    if 'LA' in r.keys():
		    for lang in r['LA']:
			    l = g.language.create(cit, organization)
			    l.language = lang
			    l.save()


        # journal
        if 'JID' in r.keys():
            issn = r['IS'] if 'IS' in r.keys() else None

            journal = Journal.get_or_create(issn             = issn,
					    title            = r['JT'],
					    iso_abbreviation = r['TA'],
					    country          = r['PL'] )
	    published = g.published_in.create(cit, journal)
	    # dates
	    if 'CRDT' in r.keys():
		    conv = time.strptime( r['CRDT'][0], "%Y/%m/%d %H:%M" )
		    published.date_created          = datetime.datetime(*conv[:6])
	    if 'DCOM' in r.keys():
		    # 'DCOM': '19990406'
		    conv = time.strptime( r['DCOM'], "%Y%m%d" )
		    published.date_completed        = datetime.datetime(*conv[:6])
	    if 'LR' in r.keys():
		    conv = time.strptime( r['LR'], "%Y%m%d" )
		    published.date_revised          = datetime.datetime(*conv[:6])
	    if 'DEP' in r.keys():
		    conv = time.strptime( r['DEP'], "%Y%m%d" )
		    published.date_electronic_publication = datetime.datetime(*conv[:6])
	    published.save()


