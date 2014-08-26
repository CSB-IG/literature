#/usr/bin/python

import nltk


a = open('capitulo_1.txt').read()

text = nltk.Text(nltk.word_tokenize(a))

keys = ['Chapo','Joaquin','Guzman','Loera']

indices = []
for name in keys:
  print  indices.append( [i for i, j in enumerate(text) if j == name] )

dictionary = dict(zip(keys,indices))

print dictionary
