import argparse

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
    
import pprint
pprint.pprint(places)