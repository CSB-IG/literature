from mongoengine import *


#############################
# Incomplete Citation Model #
#############################
class Citation(Document):
    pmid      = IntField(required=True) # PMID
    title     = StringField() # TI
    abstract  = StringField() # AB



    # dates
    date_created                = DateTimeField() # CRDT
    date_completed              = DateTimeField() # DCOM
    date_revised                = DateTimeField() # LR
    date_electronic_publication = DateTimeField() # DEP

    affiliation                 = StringField() # CI
    
    pub_types                   = ListField(StringField(), default=list)
    authors                     = ListField(StringField(), default=list)
    languages                   = ListField(StringField(), default=list)
    meshterms                   = ListField(StringField(), default=list)

