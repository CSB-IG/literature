import matplotlib
matplotlib.use('agg')
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import argparse
import pprint

parser = argparse.ArgumentParser(description='Find character names in text blobs.')

parser.add_argument('--text', type=argparse.FileType('r'), required=True, help='find names here')
parser.add_argument('--nnps', type=argparse.FileType('r'), required=True, help='tokens tagged NNP')

args   = parser.parse_args()


names = [name.strip() for name in args.nnps.readlines()]


seek_for = []
for l in range(4,0,-1):
    for i in range(0,len(names)):
        name_pile = []

        if i+l<len(names):
            for j in range(i,i+l):
                name_pile.append( names[j] )
        else:
            for j in range(i,len(names)):
                name_pile.append( names[j] )

        seek_for.append(" ".join(name_pile))



text = args.text.read()

places = {}
for name in seek_for:
    if name in places:
        offset = text.find(name, places[name][-1]+1)
        if offset != -1:
            places[name].append(offset)
    else:
        offset = text.find(name)
        if offset != -1:
            places[name] = [offset, ]



bin_width=len(text)/50


appearances = {}
for character in places:
    if len(places[character])>5:
        appearances[character]=[]
        for i in range(0,len(text),bin_width):
            app = 0
            for place in places[character]:
                if place>=i and place<=i+bin_width:
                    app+=1
            appearances[character].append(app)

#pprint.pprint(appearances)
            

colors = list(cm.rainbow(np.linspace(0, 1, len(appearances.keys()))))

for ch in appearances:
    plt.plot(range(0,len(text),bin_width),appearances[ch], label=ch, color=colors.pop())

legend = plt.legend(loc='right', shadow=True, fontsize='x-small')

fig = plt.gcf()
fig.set_size_inches(16, 13)

plt.savefig('aguas.png')
