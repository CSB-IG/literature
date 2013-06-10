# loads sqlite database from medline.txt file

from elixir import *
from models.medline import *
import time, datetime
import pprint
from sqlalchemy.exc import IntegrityError

metadata.bind = 'mysql+oursql://caopsci:G@localhost/medline'

setup_all()
create_all()


def get_or_create( model, fields):

    q = model.query.filter_by(**fields)
    
    if q.count():
        instance = q.one()
    else:
        instance = model()
        instance.from_dict( fields )
        instance.merge()

    return instance


#
# abrimos archivo plano
#
from Bio import Medline

records = Medline.parse( open("../Data/medline.txt") )
for r in records:
    try:
        cit = Citation()
        cit.pmid                  = r['PMID']

        if 'TI' in r.keys():
            cit.article_title         = r['TI'] 
        if 'AD' in r.keys():
            cit.affiliation           = r['AD'] 
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
                pt = get_or_create(PubType, {'pub_type': pub_type})                
                cit.pub_types.append( pt )

        # authors
        if 'AU' in r.keys():
            for i, author in enumerate(r['AU']):
                if author !=  'et al.':
                    a = get_or_create(Author, {'name': author,
                                               'full_name': r['FAU'][i] })
                    cit.authors.append( a )

        # language
        if 'LA' in r.keys():
            for lang in r['LA']:
                l = get_or_create( Language, {'language': lang} )
                cit.languages.append( l )


        # journal
        if 'JID' in r.keys():
            if 'IS' in r.keys():
                issn = r['IS']
            else:
                issn = None

            if 'VI' in r.keys():
                volume = r['VI']
            else:
                volume = None
            if 'IP' in r.keys():
                issue      = r['IP']
            else:
                issue = None

            journal = get_or_create(Journal, { 'jid': r['JID'],
                                               'issn' : issn,
                                               'volume' : volume,
                                               'issue' : issue,
                                               'title' : r['JT'],
                                               'iso_abbreviation' : r['TA'],
                                               'country' : r['PL'] } )
            cit.journal = journal

        session.commit()
    except IntegrityError as e:
        pprint.pprint(e)
        print r
        print
        print
        session.rollback()
        
    # mesh terms
    # if 'MH' in r.keys():
    #     for mh in r['MH']:
    #         for i, subterm in  enumerate(mh.split('/')):

    #             if subterm[0] == '*':
    #                 major = True
    #             else:
    #                 major = False

    #             if i == 0:
    #                 msh = get_or_create( session, Meshterm,
    #                                      term = subterm,
    #                                      major = major,
    #                                      other = False)
    #                 session.commit()
    #             else:
    #                 sh = get_or_create( session, Subheading,
    #                                     term = subterm,
    #                                     major = major,
    #                                     meshterm = msh.msh_id)

    #     cit.terms.append(mh)

    # # other terms
    # if 'OT' in r.keys():
    #     for mh in r['OT']:
    #         for i, subterm in  enumerate(mh.split('/')):

    #             if subterm[0] == '*':
    #                 major = True
    #             else:
    #                 major = False

    #             if i == 0:
    #                 msh = get_or_create( session, Otherterm,
    #                                      term = subterm,
    #                                      major = major,
    #                                      other = True)
    #                 session.commit()
    #             else:
    #                 sh = get_or_create( session, Subheading,
    #                                     term = subterm,
    #                                     major = major,
    #                                     meshterm = msh)


