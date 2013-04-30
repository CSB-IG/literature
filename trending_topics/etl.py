from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import time, datetime

engine = create_engine('sqlite:///Data/medline.db', echo=False)

metadata = MetaData()
metadata.bind = engine


#
# Declaramos tablas y sus relaciones
#
Base = declarative_base()

citation_author = Table('citation_author', Base.metadata,
                        Column('citations_pmid', Integer, ForeignKey('citations.pmid')),
                        Column('authors_author_id', Integer, ForeignKey('authors.author_id')))

citation_meshterm = Table('citation_meshterm', Base.metadata,
                        Column('citations_pmid', Integer, ForeignKey('citations.pmid')),
                        Column('meshterm_msh_id', Integer, ForeignKey('meshterm.msh_id')))


class Citation(Base):
    __tablename__ = 'citations'

    pmid                        = Column(Integer, primary_key=True) # PMID
    date_created                = Column(Date) # CRDT
    date_completed              = Column(Date) # DCOM
    date_revised                = Column(Date) # LR
    date_electronic_publication = Column(Date) # DEP

    
    article_title               = Column(String) # TI
    affiliation                 = Column(String) # AD
    abstract                    = Column(String) # AB
    publication_type            = Column(String) # PT
    pagination                  = Column(String) # PG
    copyright_information       = Column(String) # CI

    history_status              = relationship("Status")
    journal                     = Column(Integer, ForeignKey('journals.journal_id'))
    language                    = Column(Integer, ForeignKey('languages.language_id'))
    
    authors                     = relationship("Author",
                                               secondary=citation_author,
                                               backref="parents")

    terms                       = relationship("Meshterm",
                                               secondary=citation_meshterm,
                                               backref="parents")


class Author(Base):
    __tablename__ = 'authors'
    author_id = Column(Integer, primary_key=True)
    name      = Column(String) # AU
    full_name = Column(String) # FAU

class Journal(Base):
    __tablename__ = 'journals'
    journal_id = Column(Integer, primary_key=True) # JID
    issn = Column(String) # IS
    volume = Column(String) # VI
    issue = Column(String) # IP
    pub_date = Column(Date) # 
    title = Column(String) # JT
    iso_abbreviation = Column(String) # TA
    country = Column(String) # PL

class Status(Base):
    __tablename__ = 'status'
    phst_id = Column(Integer, primary_key=True)
    status = Column(String)
    date = Column(Date)
    pmid = Column(Integer, ForeignKey('citations.pmid'))

class Language(Base):
    __tablename__ = 'languages'
    language_id = Column(Integer, primary_key=True)
    language = Column(String) # LA


class Meshterm(Base):
    __tablename__ = 'meshterm'
    msh_id = Column(Integer, primary_key=True)
    term   = Column(String)
    major  = Column(Boolean)
    other  = Column(Boolean)



class Subheading(Base):
    __tablename__ = 'subheading'
    sh_id    = Column(Integer, primary_key=True)
    term     = Column(String)
    major    = Column(Boolean)
    meshterm = Column(Integer, ForeignKey('meshterm.msh_id'))




def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        return instance


# crear las tablas en el archivo de sqlite
Base.metadata.create_all(engine)




#
# Sesion para carga de medline
#
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

#
# abrimos archivo plano
#
from Bio import Medline

records = Medline.parse( open("Data/medline/46.txt") )
for r in records:
    
    cit = Citation()
    cit.pmid                  = r['PMID']

    if 'TI' in r.keys():
        cit.article_title         = r['TI'] 
    if 'AD' in r.keys():
        cit.affiliation           = r['AD'] 
    if 'AB' in r.keys():
        cit.abstract              = r['AB'] 
    if 'PT' in r.keys():
        cit.publication_type      = r['PT'] 
    if 'PG' in r.keys():
        cit.pagination            = r['PG'] 
    if 'CI' in r.keys():
        cit.copyright_information = r['CI'] 

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
        cit.date_electronic_publication = r['DEP'] 

    # authors
    if 'AU' in r.keys():
        # create authors
        for i, autor in enumerate(r['AU']):
            if autor !=  'et al.':
                a = get_or_create( session, Author, name=autor, full_name=r['FAU'][i])
                cit.authors.append(a)
        
    # language
    if 'LA' in r.keys():
        for i, lang in enumerate(r['LA']):
            l = get_or_create( session, Language, language=lang)
            cit.language = l


    # journal
    if 'JID' in r.keys():
        j = get_or_create( session, Journal,
                           journal_id = r['JID'],
                           issn       = r['IS'],
                           volume     = r['VI'],
                           issue      = r['IP'],
                           title      = r['JT'],
                           iso_abbreviation = r['TA'],
                           country    = r['PL'] )
        cit.journal = j

    
    # mesh terms
    if 'MH' in r.keys():
        for mh in r['MH']:
            for i, subterm in  enumerate(mh.split('/')):

                if subterm[0] == '*':
                    major = True
                else:
                    major = False

                if i == 0:
                    msh = get_or_create( session, Meshterm,
                                         term = subterm,
                                         major = major,
                                         other = False)
                    session.commit()
                else:
                    sh = get_or_create( session, Subheading,
                                        term = subterm,
                                        major = major,
                                        meshterm = msh.msh_id)

        cit.terms.append(mh)

    # other terms
    if 'OT' in r.keys():
        for mh in r['OT']:
            for i, subterm in  enumerate(mh.split('/')):

                if subterm[0] == '*':
                    major = True
                else:
                    major = False

                if i == 0:
                    msh = get_or_create( session, Otherterm,
                                         term = subterm,
                                         major = major,
                                         other = True)
                    session.commit()
                else:
                    sh = get_or_create( session, Subheading,
                                        term = subterm,
                                        major = major,
                                        meshterm = msh)

        cit.terms.append(mh)
        session.add(cit)
        session.commit()

