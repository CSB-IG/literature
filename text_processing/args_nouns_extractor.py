# coding: utf-8
#!/usr/bin/python

import argparse
import nltk
from nltk.tag import pos_tag
import sys

parser = argparse.ArgumentParser(description='Tags and extract words such as nouns or verbs.') 

parser.add_argument('--infile', type=argparse.FileType('r'), required=True )
parser.add_argument('--tag', type=str, required=True )
parser.add_argument('--length', type=int, required=True )

args = parser.parse_args()
infile = args.infile.read().decode('utf8')

text = nltk.Text(nltk.word_tokenize( infile ))

tagged_sent = pos_tag(text)

tags = [word for word,pos in tagged_sent if pos == args.tag and len(word)>args.length]

#long_words = [words for words in tags if len(words) > args.length]


for w in tags:
    if w.istitle() == True:
        try:
            print w
        except:
            pass

