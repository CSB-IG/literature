# coding: utf-8
import argparse
from pattern.es import parsetree
from pattern.vector import Document
import json
from operator import itemgetter
from itertools import groupby

from pprint import pprint

parser = argparse.ArgumentParser(description='Find character names in text blobs. Create graph.')

parser.add_argument('--text', type=argparse.FileType('r'), required=True, help='find names here')

args   = parser.parse_args()

        
s = parsetree(args.text.read(), relations=True, lemmata=True)


for i in range(len(s)):
    sentence = s[i]
    print "[%s]"%i, s[i].string.encode('utf8')


