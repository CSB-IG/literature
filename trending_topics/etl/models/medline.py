from elixir import *


class Citation(Entity):
    pmid                        = Field(Integer, primary_key=True) # PMID
    article_title               = Field(UnicodeText) # TI
    affiliation                 = Field(UnicodeText) # AD
    abstract                    = Field(UnicodeText) # AB
    pagination                  = Field(UnicodeText) # PG
    copyright_information       = Field(UnicodeText) # CI

    # dates
    date_created                = Field(DateTime) # CRDT
    date_completed              = Field(DateTime) # DCOM
    date_revised                = Field(DateTime) # LR
    date_electronic_publication = Field(DateTime) # DEP

    # relationships
    journal                     = ManyToOne('Journal')
    pub_types                   = ManyToMany('PubType')    
    authors                     = ManyToMany('Author')    
    languages                   = ManyToMany('Language')

    def __repr__(self):
        return '<Cit #%d %s>' % (self.pmid, self.article_title)


    # terms                       = relationship("Meshterm",
    #                                            secondary=citation_meshterm,
    #                                            backref="parents")


class PubType(Entity):
    pub_type = Field(UnicodeText) # PT
    citations = ManyToMany('Citation')    

    def __repr__(self):
        return '<PubType #%d %s>' % (self.id, self.pub_type)

class Author(Entity):
    name      = Field(UnicodeText) # AU
    full_name = Field(UnicodeText) # FAU
    citations = ManyToMany('Citation')
    def __repr__(self):
        return '<Author #%d %s>' % (self.id, self.name)


class Journal(Entity):
    jid  = Field(Integer) # JID
    issn = Field(UnicodeText) # IS
    volume = Field(UnicodeText) # VI
    issue = Field(UnicodeText) # IP
    pub_date = Field(DateTime) # 
    title = Field(UnicodeText) # JT
    iso_abbreviation = Field(UnicodeText) # TA
    country = Field(UnicodeText) # PL
    citations = OneToMany('Citation')
    def __repr__(self):
        return '<Journal #%d %s>' % (self.id, self.title)


class Language(Entity):
    language = Field(UnicodeText) # LA
    citations = ManyToMany('Citation')
    def __repr__(self):
        return '<Language #%d %s>' % (self.id, self.language)

# class Meshterm(Entity):
#     msh_id = Field(Integer, primary_key=True)
#     term   = Field(UnicodeText)
#     major  = Field(Boolean)
#     other  = Field(Boolean)



# class Subheading(Entity):
#     sh_id    = Field(Integer, primary_key=True)
#     term     = Field(UnicodeText)
#     major    = Field(Boolean)
#     meshterm = Field(Integer, ForeignKey('meshterm.msh_id'))
