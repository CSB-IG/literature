#!/usr/bin/python

import nltk


Text = nltk.Text(nltk.tokenize.RegexpTokenizer(r'\w+').tokenize( open('IBT_titulos_1983_2014feb.txt').read() ))

words = [w.lower() for w in Text]

string_of_words = ' '.join( words )

text = nltk.Text(nltk.tokenize.RegexpTokenizer(r'\w+').tokenize( string_of_words ))

text.collocations(400, 2)


