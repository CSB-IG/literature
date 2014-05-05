import nltk
from nltk.tag import pos_tag

a = open('IBT_titulos_1983_2014feb.txt').read()

text = nltk.Text(nltk.word_tokenize(a))

tagged_sent = pos_tag(text)

tags = [word for word,pos in tagged_sent if pos == 'VBD']

long_words = [words for words in tags if len(words) > 3]

Capitals = []

for w in long_words:
    if w.istitle() == True:
        Capitals.append( w )
print Capitals
