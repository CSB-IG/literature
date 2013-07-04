from elixir import *
from models.medline import *
from random import shuffle

metadata.bind = 'mysql+oursql://caopsci:G@localhost/medline'

setup_all()


for b in Branch.query.all():
    levels = len(b.branch.split('.'))
    print b.branch[:1], b.id, b.id+1, levels
