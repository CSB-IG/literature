#!/usr/bin/python

import argparse
import nltk
import sys
from collocations import extract


parser = argparse.ArgumentParser(description='Find pairs of words in co-location within texts.')
parser.add_argument('--outfile', type=argparse.FileType('w'), required=False,
                    default=sys.stdout)
parser.add_argument('--infile', type=argparse.FileType('r'), required=True )
parser.add_argument('--length', type=int, required=True )
parser.add_argument('--freq', type=int, required=True )
parser.add_argument('--bigrams', type=int, required=True )



if __name__ == '__main__':
    args    = parser.parse_args()
    infile  = args.infile.read()

    with args.outfile as f:
        for par in extract( nltk.tokenize.RegexpTokenizer( r'\w+').tokenize( infile ),
                            args.length,
                            args.freq,
                            args.bigrams ):
            f.write( "%s, %s\n" % (par) )
