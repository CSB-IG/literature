from jinja2 import Environment, FileSystemLoader
import os, shutil


env = Environment(loader=FileSystemLoader('templates'))
circos_conf = env.get_template('circos.conf')


karyotype = [
    {'name': 'A', 'start': 1,     'end': 2903,  'color': 'ylorrd-9-seq-1', 'z':0},
    {'name': 'B', 'start': 2904,  'end': 8077,  'color': 'ylorrd-9-seq-2', 'z':1},
    {'name': 'C', 'start': 8078,  'end': 19331, 'color': 'gnbu-9-seq-3', 'z':2},
    {'name': 'D', 'start': 19332, 'end': 39983, 'color': 'gnbu-9-seq-4', 'z':3},
    {'name': 'E', 'start': 39984, 'end': 44710, 'color': 'gnbu-9-seq-5', 'z':4},
    {'name': 'F', 'start': 44711, 'end': 45841, 'color': 'gnbu-9-seq-6', 'z':5},
    {'name': 'G', 'start': 45842, 'end': 49210, 'color': 'gnbu-9-seq-7', 'z':6},
    {'name': 'H', 'start': 49211, 'end': 49708, 'color': 'gnbu-9-seq-8', 'z':7},
    {'name': 'I', 'start': 49709, 'end': 50333, 'color': 'gnbu-9-seq-9', 'z':8},
    {'name': 'J', 'start': 50334, 'end': 50932, 'color': 'reds-9-seq-9', 'z':9},
    {'name': 'K', 'start': 50933, 'end': 51149, 'color': 'reds-9-seq-8', 'z':10},
    {'name': 'L', 'start': 51150, 'end': 51655, 'color': 'reds-9-seq-7', 'z':11},
    {'name': 'M', 'start': 51656, 'end': 51901, 'color': 'reds-9-seq-6', 'z':12},
    {'name': 'N', 'start': 51902, 'end': 54204, 'color': 'reds-9-seq-5', 'z':13},
    {'name': 'V', 'start': 54205, 'end': 54388, 'color': 'reds-9-seq-4', 'z':14},
    {'name': 'Z', 'start': 54389, 'end': 54935, 'color': 'reds-9-seq-3', 'z':15},
    ]


with open('data/karyotype/karyotype.meshtree.txt', 'w') as f:
    for contig in karyotype:
        f.write( "chr - %s %s %s %s %s\n" % (contig['name' ],
                                           contig['name' ],
                                           contig['start'],
                                           contig['end'  ],
                                           contig['color']) )

data_path = "/home/rgarcia/caopsci/trending_topics/Data/circos"

for year in range(1987,2014):
    os.makedirs(str(year))

    shutil.copy('templates/bands.conf', str(year) )
    shutil.copy('templates/ideogram.conf', str(year) )
    shutil.copy('templates/ideogram.label.conf', str(year) )
    shutil.copy('templates/ideogram.position.conf', str(year) )
    

    with open(str(year)+'/circos.conf', 'w') as f:
        f.write( circos_conf.render( citation_depth = data_path+'/citation_depth_'+str(year)+'.tsv',
                                     links          = data_path+'/branch_nx_l3_'+str(year)+'.links',
                                     contigs        = karyotype ) )
