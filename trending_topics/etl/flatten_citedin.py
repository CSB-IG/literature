import sys

input_file = sys.argv[1]

cited = input_file.split('.')[0]


f = open(input_file, 'r')
l = f.readlines()
f.close()

citing = l[0].split(',')

citing.pop()

for c in citing:
    print "%s, %s" % ( cited, c )
