import fileinput
from pprint import pprint

# dictionary of last names
apellidos = [a.strip() for a in open('/home/rgarcia/literature/text_processing/data/nombres_verbos/apellidos_uniq.txt').readlines()]


# load text into list
textv = []
for line in fileinput.input():
    for w in line.split():
        textv.append(w.replace(',','').replace('"',''))

# find indexes for names in last-name dictionary
name_indexes = []
for n in range(len(textv)):
    w = textv[n]
    if w.upper() in apellidos:
        if w[0].isupper() and len(w)>3:
            name_indexes.append(n)



# find indexes of periods
periods = []
for n in range(len(textv)):
    w = textv[n]
    if w.endswith('.'):
        periods.append(n)

pprint(periods)

#for i in name_indexes:
#    print textv[i-2],textv[i-1],textv[i],textv[i+1],textv[i+2],textv[i+3]

