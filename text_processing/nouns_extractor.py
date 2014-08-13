import argparse
from pymongo import MongoClient, collection
import nltk
from nltk.tag import pos_tag


parser = argparse.ArgumentParser(description='Tokenize text, load it into mongoDB.')

parser.add_argument('--uri', type=str, required=True, help='DB uri, e.g. mongodb://localhost:27017/my_database')
parser.add_argument('--collection', type=str, required=True, help='MongoDB collection, e.g. the name of the text')
parser.add_argument('--text', type=argparse.FileType('r'), required=True, help='Text to tokenize')

args   = parser.parse_args()

client = MongoClient(args.uri)
db     = client.get_default_database()
collec = collection.Collection( db, args.collection )

text = nltk.Text(nltk.word_tokenize(args.text.read()))

tagged = pos_tag(text)

for i in range(0,len(tagged)):
    (token, tag) = tagged[i]

    token_dict = { 'index': i,
                   'token': token,
                   'tag'  : tag, }
    
    collec.save(token_dict)

