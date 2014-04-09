#!/usr/bin/python

import nltk


raw = open('Gomorra.txt').read()

tokens = nltk.tokenize.RegexpTokenizer(r'\w+').tokenize(raw)

pairs = nltk.bigrams(tokens)
bigrams_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
finder = nltk.collocations.BigramCollocationFinder.from_words(pairs)
finder.apply_freq_filter(3)
finder.nbest(bigrams_measures.pmi, 200)

##To-do: remove articles and words like in, and, or, on, etc. Use
##argparse to input a path to a file and the number of pairs to
##return. Print the frequency of each collocation. Return it to a
##file.csv or file.txt. For spanish it needs the right codification utf-8 or whatever is needed.

