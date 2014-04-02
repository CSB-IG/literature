from elixir import *



class Citation(Entity):
    pmid                        = Field(Integer, primary_key=True) # PMID
    article_title               = Field(UnicodeText(5534)) # TI

    abstract                    = Field(UnicodeText(65534)) # AB
    pagination                  = Field(UnicodeText(1534)) # PG
    copyright_information       = Field(UnicodeText(5534)) # CI

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
    affiliation                 = ManyToOne('Organization') # AD

    meshterms                   = ManyToMany('TermCitation')

    cited_in                    = ManyToMany('Citation')

    
    def country(self):
        return self.journal.country

    def __repr__(self):
        title = self.article_title[:35] + (self.article_title[35:] and '..')
        return '<Cit #%d %s>' % (self.pmid, self.article_title)




class Organization(Entity):
    name      = Field(UnicodeText(2000))
    citations = OneToMany('Citation')
    def __repr__(self):
        return '<Org #%d %s>' % (self.id, self.name)

class PubType(Entity):
    pub_type = Field(UnicodeText(255)) # PT
    citations = ManyToMany('Citation',
                           tablename='pub_type_citation')    

    def __repr__(self):
        return '<PubType #%d %s>' % (self.id, self.pub_type)

class Author(Entity):
    name      = Field(UnicodeText(534)) # AU
    full_name = Field(UnicodeText(534)) # FAU
    citations = ManyToMany('Citation')

    def fitness(self):
        pass

    def __repr__(self):
        return '<Author #%d %s>' % (self.id, self.name)


class Journal(Entity):
    jid  = Field(UnicodeText(534)) # JID
    issn = Field(UnicodeText(1534)) # IS
    volume = Field(UnicodeText(534)) # VI
    issue = Field(UnicodeText(534)) # IP
    pub_date = Field(DateTime) # 
    title = Field(UnicodeText(255)) # JT
    iso_abbreviation = Field(UnicodeText(534)) # TA
    country = Field(UnicodeText(534)) # PL
    citations = OneToMany('Citation')
    def __repr__(self):
        return '<Journal #%d %s>' % (self.id, self.title)


class Language(Entity):
    language = Field(UnicodeText(200)) # LA
    citations = ManyToMany('Citation',
                           tablename='lan_cit')
    def __repr__(self):
        return '<Language #%d %s>' % (self.id, self.language)



class Subheading(Entity):
    sh    = Field(UnicodeText(255))
    cited = OneToMany('SubheadingTerm')
    def __repr__(self):
        return '<SH #%d %s>' % (self.id, self.sh)

    
class SubheadingTerm(Entity):
    sh = ManyToOne('Subheading')
    termcitation = ManyToOne('TermCitation')
    major = Field(Boolean)
    def __repr__(self):
        if self.major:
            return '<SH #%d *%s @ %s>' % (self.id, self.sh.sh, self.termcitation)
        else:
            return '<SH #%d %s @ %s>' % (self.id, self.sh.sh, self.termcitation)             


class Meshterm(Entity):
    term     = Field(UnicodeText(255)) 
    branches = OneToMany('Branch')
    cited    = OneToMany('TermCitation')
    def __repr__(self):
        return '<MshTrm #%d %s>' % (self.id, self.term)


class Branch(Entity):
    branch = Field(UnicodeText(1534))
    term   = ManyToOne('Meshterm')
    def __repr__(self):
        return '<branch #%d %s @ %s>' % (self.id, self.branch, self.term.term)


class TermCitation(Entity):
    major       = Field(Boolean)
    term        = ManyToOne('Meshterm')
    subheadings = OneToMany('SubheadingTerm')
    citation    = ManyToOne('Citation')
    def __repr__(self):
        if self.major:
            return '<MH #%d *%s @ %s>' % (self.term.id, self.term.term, self.citation.pmid)
        else:
            return '<MH #%d %s @ %s>' % (self.term.id, self.term.term, self.citation.pmid)    








def test():
    global session, cit1, cit2, cit3
    
    cit1 = Citation(pmid=1, article_title='cave canem')
    cit2 = Citation(pmid=2, article_title='cave guajolotem')
    cit3 = Citation(mpid=3, article_title='animalae sunt malorum')

    cit2.references.append(cit1)
    cit3.references = [ cit1, cit2 ]
    
    session.commit()
