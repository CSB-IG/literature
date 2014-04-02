
f = open('/media/JMS/Trending_topics/networks/00.csv')
network_file = f.readlines()
f.close()


import pprint


count = {}

for line in network_file:
    (date, mh1, pmid, mh2) = line.split('|')
    
    if mh1 in count:
        if mh2 in count[mh1]:
            count[mh1][mh2] += 1
        else:
            count[mh1][mh2] = 1
    else:
        count[mh1] = { mh2: 1 }



# pprint.pprint(count)

for mh1 in count:
    for mh2 in count[mh1]:
        print "%s %s %s" % (count[mh1][mh2], mh1, mh2)


