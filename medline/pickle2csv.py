#!/usr/bin/env python
import argparse
import csv
import networkx as nx
import sys

parser = argparse.ArgumentParser(description='Convert from pickle format to CSV')
parser.add_argument('--pickle', type=argparse.FileType('r'), required=True)
parser.add_argument('--csv',    type=argparse.FileType('w'), default=sys.stdout)
args    = parser.parse_args()


with args.csv as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)

    g = nx.gpickle.read_gpickle(args.pickle)
    
    for e in g.edges():
        spamwriter.writerow([e[0], e[1]])
