# loads sqlite database from medline.txt file

from elixir import *
from models.medline import *
import time, datetime
import pprint
from sqlalchemy.exc import IntegrityError

metadata.bind = 'mysql+oursql://caopsci:G@localhost/medline'

setup_all()
create_all()





#
# abrimos archivo plano de meshterms
#
from Bio import Medline

f =open("../Data/meshterms.txt", 'r')
lineas = f.readlines()
f.close()

for l in lineas:
    if l.startswith('MH ='):
        (tag, mh) = l.split(' = ')
        msh = Meshterm()
        msh.term = mh.rstrip()
        msh.merge()
        print "%s, %s, %s" % (msh.id, msh.term, mh.rstrip())
        session.commit()

    
#
#cargamos el diccionario de branches
#
f = open("../Data/mtrees2013.bin", 'r')
lines = f.readlines()
f.close()
for line in lines:
    (term, branch) = line.split(';')
    mh = Meshterm.get_by(term=term.rstrip())
    if mh:
        mh.branches.append(Branch(branch=branch))
        mh.merge()
    else:
        print "falta "+term
    session.commit()



#
# cargamos subheadings
#
f = open("../Data/d2013.bin", 'r')
lines = f.readlines()
f.close()
for l in lines:
    if l.startswith('MH ='):
        (tag, mh) = l.split(' = ')
        sh = Subheading()
        sh.sh = mh.rstrip()
        sh.merge()
        print "%s, %s, %s" % (sh.id, sh.sh, mh.rstrip())
        session.commit()
