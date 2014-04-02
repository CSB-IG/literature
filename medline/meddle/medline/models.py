from django.db import models

# computes jacard index for two sets
def jaccard_index( a, b):
    return float(len(a.intersection(b))) / float(len(a.union(b)))



class Meshterm(models.Model):
    term     = models.CharField(max_length=255)
    def __unicode__(self):
        return '#%d %s' % (self.id, self.term)


class Branch(models.Model):
    branch = models.CharField(max_length=1534)
    term   = models.ForeignKey('Meshterm')

    def root(self):
        return self.branch[:1]
    
    def __unicode__(self):
        return '#%d %s' % (self.id, self.branch)


class Subheading(models.Model):
    term     = models.CharField(max_length=255)
    def __unicode__(self):
        return '#%d %s' % (self.id, self.term)


class Meshcitation(models.Model):
    meshterm   = models.ForeignKey(Meshterm)
    citation   = models.ForeignKey('Citation')
    major      = models.BooleanField()

    subheadings = models.ManyToManyField(Subheading, through='Subheadingterm')


    def __unicode__(self):
        major = '*' if self.major else ''
        subheadings = []
        for sh in self.subheadingterm_set.all():
            submajor = '*' if sh.major else ''
            subheadings.append(submajor+sh.subheading.term)
        
        return '%s%s' % (major, '/'.join([self.meshterm.term]+subheadings))


    def majorless(self):
        subheadings = []
        for sh in self.subheadingterm_set.all():
            subheadings.append(sh.subheading.term)
        
        return '/'.join([self.meshterm.term]+subheadings)


    def mesh_set(self):
        major = '*' if self.major else ''
        term = "%s%s" % (major, self.meshterm.term)
        subheadings = []
        for sh in self.subheadingterm_set.all():
            submajor = '*' if sh.major else ''
            subheadings.append(submajor+sh.subheading.term)
        
        subheadings.append(term)
        return set(subheadings)



    def majorless_mesh_set(self):
        terms = []
        for term in self.subheadingterm_set.all():
            terms.append(term.subheading.term)
        return set(terms + [self.meshterm.term])



class Subheadingterm(models.Model):
    meshcitation   = models.ForeignKey(Meshcitation)
    subheading     = models.ForeignKey('Subheading')
    major          = models.BooleanField()
    def __unicode__(self):
        major = '*' if self.major else ''
        return '#%d %s%s' % (self.id, major, self.subheading.term)



class Journal(models.Model):
    jid              = models.CharField(max_length=534) # JID
    issn             = models.CharField(max_length=1534, null=True) # IS
    volume           = models.CharField(max_length=534, null=True) # VI
    issue            = models.CharField(max_length=534, null=True) # IP
    title            = models.CharField(max_length=255) # JT
    iso_abbreviation = models.CharField(max_length=534) # TA
    country          = models.CharField(max_length=534) # PL
    def __unicode__(self):
        return '#%d %s %s' % (self.id, self.jid, self.title)


class Organization(models.Model):
    name             = models.CharField(max_length=4000)
    def __unicode__(self):
        return '#%d %s' % (self.id, self.name)

class PubType(models.Model):
    pub_type         = models.CharField(max_length=255) # PT
    def __unicode__(self):
        return '#%d %s' % (self.id, self.pub_type)


class Author(models.Model):
    name             = models.CharField(max_length=534) # AU
    full_name        = models.CharField(max_length=534) # FAU
    def __unicode__(self):
        return '#%d %s' % (self.id, self.name)

class Language(models.Model):
    language         = models.CharField(max_length=200) # LA
    def __unicode__(self):
        return '#%d %s' % (self.id, self.language)

class Citation(models.Model):
    pmid                        = models.IntegerField(primary_key=True) # PMID
    title                       = models.CharField(max_length=5534) # TI

    abstract                    = models.TextField(null=True) # AB
    pagination                  = models.CharField(max_length=1534, null=True) # PG
    copyright_information       = models.CharField(max_length=5534, null=True) # CI

    # dates
    date_created                = models.DateTimeField(null=True) # CRDT
    date_completed              = models.DateTimeField(null=True) # DCOM
    date_revised                = models.DateTimeField(null=True) # LR
    date_electronic_publication = models.DateTimeField(null=True) # DEP

    # relationships
    journal                     = models.ForeignKey(Journal,      null=True, blank=True, default=None)
    affiliation                 = models.ForeignKey(Organization, null=True, blank=True, default=None) # AD
    
    pub_types                   = models.ManyToManyField(PubType)
    authors                     = models.ManyToManyField(Author) 
    languages                   = models.ManyToManyField(Language)

    meshterms                   = models.ManyToManyField(Meshterm, through='Meshcitation')

    cited_in                    = models.ManyToManyField('self')

    def major_terms(self):
        return [n.meshterm for n in self.meshcitation_set.filter(major=True)]

    def bag_of_words(self):
        bow=[]
        for mc in self.meshcitation_set.all():
            bow += list(mc.majorless_mesh_set())
        return set(bow)

    def __unicode__(self):
        return '#%d %s' % (self.pmid, self.title)







#import django_filters

# class CitationFilter(django_filters.FilterSet):
#     class Meta:
#         model  = Citation
#         fields = ['meshterms']
