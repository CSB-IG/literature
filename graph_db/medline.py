from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime
from bulbs.utils import current_datetime


# citations are published in journals
class PublishedIn(Relationship):
    label = "published_in"
    # dates
    date_created                = DateTime() # CRDT
    date_completed              = DateTime() # DCOM
    date_revised                = DateTime() # LR
    date_electronic_publication = DateTime() # DEP
    

# citations cite other citations
class CitedIn(Relationship):
    pass

class Citation(Node):
    pmid                        = Integer(nullable=False) # PMID
    article_title               = String(nullable=False) # TI

    abstract                    = String() # AB
    pagination                  = String() # PG
    copyright_information       = String() # CI

    pub_type = String() # PT



class Organization(Node):
    name      = String()


class Author(Node):
    name      = String() # AU
    full_name = String() # FAU

class Journal(Node):
    jid  = String() # JID
    issn = String(nullable=True) # IS
    volume = String() # VI
    issue = String() # IP
    title = String() # JT
    iso_abbreviation = String() # TA
    country = String() # PL


# authors write citations in languages
class Language(Relationship):
    language = String()


# mesh terms describe citations
class Describes(Relationship):
    major = String()


class Meshterm(Node):
    term     = String() 


# branches classify meshterms
class ClassifiedIn(Relationship):
    pass

class Branch(Node):
    branch = String()



