from elixir import *
from models.medline import *
from sqlalchemy.exc import IntegrityError

metadata.bind = 'mysql+oursql://caopsci:G@localhost/medline'

setup_all()





f = open('../Data/citedin.csv', 'r')
pairs = f.readlines()
f.close()


citation = Citation()

for pair in pairs:
    (pmid, citedin) = pair.split(',')

    try:
        if pmid != citation.pmid:
            citation = Citation.get_by(pmid=pmid)
        
        cited_in = Citation.get_by(pmid=citedin)
        if cited_in:
            citation.cited_in.append( cited_in )
            session.commit()
            print "%s cited in %s" % (citation.pmid, cited_in.pmid)
            
    except IntegrityError as e:
        print "ERROR"
        pprint.pprint(e)
        pprint.pprint(pair)
        session.rollback()
        print "/ERROR"
    
