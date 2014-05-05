#!/usr/bin/python

import argparse
import nltk
from nltk.tag import pos_tag
import sys

parser = argparse.ArgumentParser(description='Tags and extract words such as nouns or verbs.') 

parser.add_argument('--infile', type=argparse.FileType('r'), required=True )
parser.add_argument('--outfile', type=argparse.FileType('w'), required=False, default=sys.stdout)
parser.add_argument('--tag', type=str, required=True )
parser.add_argument('--length', type=int, required=True )

#a = open('capitulo_1.txt').read()
args = parser.parse_args()
infile = args.infile.read()
#outfile = args.outfile.write()

text = nltk.Text(nltk.word_tokenize( infile ))

tagged_sent = pos_tag(text)

tags = [word for word,pos in tagged_sent if pos == args.tag]

long_words = [words for words in tags if len(words) > args.length]

#print tags[0:20]

Tagged_words = []

for w in long_words:
    if w.istitle() == True:
        Tagged_words.append( w )
print Tagged_words
