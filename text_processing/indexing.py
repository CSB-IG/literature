#/usr/bin/python

import nltk


a = open('capitulo_1.txt').read()

text = nltk.Text(nltk.word_tokenize(a))

keys = ['Chapo','Joaquin','Guzman','Loera']

values = []

for i in keys:
    values.append(text.index(i))

dictionary = dict(zip(keys,values))

print dictionary
