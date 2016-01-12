

csvs = [
    'cartel_de_sinaloa.csv',
    'cartel_incomodo.csv',
    'imperio_del_chapo.csv',
    'marca_de_sangre.csv',
    'narcoleaks.csv',
    'senores_del_narco.csv',
    'ultimo_narco.csv']


edgelist = {}
for c in csvs:
    lines = open(c).readlines()
    for l in lines:
        (s,t,w) = l.strip().split(';')

        w = int(w)

        if (s,t) in edgelist:
            edgelist[(s,t)]+=w
        else:
            edgelist[(s,t)]=w


for e in edgelist:
    if edgelist[e]>=10:
        print "%s;%s;%s" % (e[0],e[1],edgelist[e])
