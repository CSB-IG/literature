from elixir import *
from models.medline import *
from random import shuffle
import sys

metadata.bind = 'mysql+oursql://caopsci:G@localhost/medline'

setup_all()

input_path = sys.argv[1]

f = open(input_path)
pares = f.readlines()
f.close()


for n,linea in enumerate(pares):
    (b1, b2, w) = linea.split(',')
    b = Branch.query.filter(Branch.branch.startswith(b1))
    start = b[0].id
    end   = b[-1].id
    print "e%s %s %s %s" % (n, b[0].branch[:1], start, end)

    b = Branch.query.filter(Branch.branch.startswith(b2))
    start = b[0].id
    end   = b[-1].id
    print "e%s %s %s %s" % (n, b[0].branch[:1], start, end)
    
