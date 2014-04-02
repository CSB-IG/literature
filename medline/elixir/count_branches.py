from elixir import *
from models.medline import *
import time, datetime
import pprint


metadata.bind = 'mysql+oursql://caopsci:G@localhost/medline'

setup_all()





for year in range(1987,2014):
    start = datetime.datetime(year,1,1)
    end   = datetime.datetime(year+1,1,1)

    year_query = Citation.query.filter(Citation.date_created>=start,
                                       Citation.date_created<=end)



    count = {}
    for cit in year_query.all():
        for mh in cit.meshterms:
            try:
                for branch in mh.term.branches:
                    key = branch.branch[:1]
                    if key in count:
                        count[key]+=1
                    else:
                        count[key]=1
            except:
                pass

    with open('root_count_'+str(year)+'.csv', 'w') as f:
        for key in count:
            f.write( "%s;%s\n" % (key, count[key] ) )
