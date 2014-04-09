#!/usr/bin/python

import nltk
import pprint

raw = open('journal.pone.0066341-1.txt').read()
token = nltk.tokenize.RegexpTokenizer(r'\w+').tokenize(raw)

def text_filter( 

text = ''
for w in token:
    if len(w) >= 4:
        #text = ''.join(w)
        #pprint.pprint( text )
        text += w + ','
    return text

#pprint.pprint( text )
