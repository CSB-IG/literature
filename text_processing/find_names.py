import argparse
from pattern.es import parsetree
from pattern.vector import Document
from pprint import pprint

parser = argparse.ArgumentParser(description='Find character names in text blobs.')

parser.add_argument('--text', type=argparse.FileType('r'), required=True, help='find names here')
parser.add_argument('--names', type=argparse.FileType('r'), required=True, help='dictionary of names')

args   = parser.parse_args()

last_names = [name.strip() for name in args.names.readlines()]

s = parsetree(args.text.read(), relations=True, lemmata=True)

all_sentences = []
for i in range(len(s)):
    sentence = s[i]
    names_in_sentence = {'sentence_index': i}
    for n in range(1,len(sentence.words)):
        last_word = sentence.words[n-1]
        lw = last_word.string
        word = sentence.words[n]
        w = word.string

        if w.upper() in last_names and w[0].isupper() and len(w)>3 and lw.upper() in last_names and lw[0].isupper() and len(lw)>3:
            if not lw in names_in_sentence.values():
                names_in_sentence[last_word.index] = lw
            if not w in names_in_sentence:
                names_in_sentence[word.index] = w

    if len(names_in_sentence.keys()) > 1:
        all_sentences.append(names_in_sentence)


pprint(all_sentences)
