# usage citation_depth.py 2011
# prints circos histogram

from elixir import *
from models.medline import *
from random import shuffle
import math, sys

metadata.bind = 'mysql+oursql://caopsci:G@localhost/medline'

setup_all()

year = sys.argv[1]

for b in Branch.query.all():
    cited = 0
    for cit in b.term.cited:
        if cit.citation.date_created.year == int(year):
            cited += 1
    if cited > 0:
        cited = math.log10(cited)
        
    print b.branch[:1],b.id,b.id+1,cited
