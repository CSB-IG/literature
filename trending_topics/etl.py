from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///Data/medline.db', echo=False)

metadata = MetaData()
metadata.bind = engine


#
# Declaramos tablas y sus relaciones
#
Base = declarative_base()

citation_author = Table('association', Base.metadata,
                        Column('citations_pmid', Integer, ForeignKey('citations.pmid')),
                        Column('authors_author_id', Integer, ForeignKey('authors.author_id')))

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
    issue = Column(String) 
    pub_date = Column(Date)
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
    cit.pmid = r['PMID']
    


# u = User('ed', 'Ed Jones', 'edspassword')
# session.add(u)
# session.commit()
