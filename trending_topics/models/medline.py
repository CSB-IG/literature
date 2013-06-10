from elixir import *



class Citation(Entity):
    pmid                        = Field(Integer, primary_key=True) # PMID
    article_title               = Field(UnicodeText(65534)) # TI
    affiliation                 = Field(UnicodeText(65534)) # AD
    abstract                    = Field(UnicodeText(65534)) # AB
    pagination                  = Field(UnicodeText(65534)) # PG
    copyright_information       = Field(UnicodeText(65534)) # CI

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

    def country(self):
        return self.journal.country

    def __repr__(self):
        title = self.article_title[:35] + (self.article_title[35:] and '..')
        return '<Cit #%d %s>' % (self.pmid, self.article_title)


    # terms                       = relationship("Meshterm",
    #                                            secondary=citation_meshterm,
    #                                            backref="parents")


class PubType(Entity):
    pub_type = Field(UnicodeText(65534)) # PT
    citations = ManyToMany('Citation',
                           tablename='pub_type_citation')    

    def __repr__(self):
        return '<PubType #%d %s>' % (self.id, self.pub_type)

class Author(Entity):
    name      = Field(UnicodeText(65534)) # AU
    full_name = Field(UnicodeText(65534)) # FAU
    citations = ManyToMany('Citation')
    def __repr__(self):
        return '<Author #%d %s>' % (self.id, self.name)
        #return '%s' % self.name

class Journal(Entity):
    jid  = Field(UnicodeText(65534)) # JID
    issn = Field(UnicodeText(65534)) # IS
    volume = Field(UnicodeText(65534)) # VI
    issue = Field(UnicodeText(65534)) # IP
    pub_date = Field(DateTime) # 
    title = Field(UnicodeText(65534)) # JT
    iso_abbreviation = Field(UnicodeText(65534)) # TA
    country = Field(UnicodeText(65534)) # PL
    citations = OneToMany('Citation')
    def __repr__(self):
        return '<Journal #%d %s>' % (self.id, self.title)


class Language(Entity):
    language = Field(UnicodeText(65534)) # LA
    citations = ManyToMany('Citation',
                           tablename='lan_cit')
    def __repr__(self):
        return '<Language #%d %s>' % (self.id, self.language)



# class TermCitation(Entity):
#     parent_id = OneToOne('TermCitation')
#     term      = OneToOne('Meshterm')

# class Meshterm(Entity):
#     term     = Field(UnicodeText(65534)) 
#     branches = OneToMany('Meshtree')

# class Meshtree(Entity):
#     branch = Field(UnicodeText(65534))
#     term   = ManyToOne('Meshterm')

#     major  = Field(Boolean)
#     other  = Field(Boolean)



# class Subheading(Entity):
#     sh_id    = Field(Integer, primary_key=True)
#     term     = Field(UnicodeText(65534))
#     major    = Field(Boolean)
#     meshterm = Field(Integer, ForeignKey('meshterm.msh_id'))
