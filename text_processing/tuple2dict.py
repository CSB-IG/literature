#!/ust/bin/python

import nltk
from nltk.tag import pos_tag

a = open('infile').read()

text = nltk.Text(nltk.word_tokenize(a))
tagged = pos_tag(text)

list_dict = [{a:b} for a, b in tagged]

m = [x for x, y in enumerate(tagged)]

print  list_dict
