import nltk
from nltk.tag import pos_tag

a = open('narco.txt').read()

text = nltk.Text(nltk.word_tokenize(a))

tagged_sent = pos_tag(text)

propernames = [word for word,pos in tagged_sent if pos == 'NNP']

long_words = [words for words in propernames if len(words) > 3]

Capitals = []

for w in long_words:
    if w.istitle() == True:
        Capitals.append( w )
print Capitals
