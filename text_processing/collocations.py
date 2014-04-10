#!/usr/bin/python

import nltk

def extract( token_list, lengths, frequency, no_bigrams ):
    text = []
    words = [w.lower() for w in token_list]
    for w in words:
        if len(w) > lengths:
            text.append(w)
    pairs = nltk.bigrams(text)
    bigrams_measures = nltk.collocations.BigramAssocMeasures()
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    finder = nltk.collocations.BigramCollocationFinder.from_words(pairs)
    finder.apply_freq_filter( frequency )
    pares =[]
    for par in finder.nbest( bigrams_measures.pmi, no_bigrams ):
        pares.append(par[0])
        pares.append(par[1])
    return pares


