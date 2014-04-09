#!/usr/bin/python

import nltk
import pprint
import argparse

raw = open('journal.pone.0066341-1.txt').read()
token = nltk.tokenize.RegexpTokenizer(r'\w+').tokenize(raw)

def text_filter( token, length, frequency, no_bigrams ):
    text = []
    for w in token:
        if len(w) > 3:
            text.append(w)
            pprint.pprint(text)
    pairs = nltk.bigrams(text)
    bigrams_measures = nltk.collocations.BigramAssocMeasures()
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    finder = nltk.collocations.BigramCollocationFinder.from_words(pairs)
    finder.apply_freq_filter( frequency )
    print finder.nbest( bigrams_measures.pmi, no_bigrams )
