from jinja2 import Environment, FileSystemLoader
import os, shutil


env = Environment(loader=FileSystemLoader('templates'))
circos_conf = env.get_template('circos.conf')


contigs = [
    {'name': 'A', 'color': 'ylorrd-9-seq-1'},
    {'name': 'B', 'color': 'ylorrd-9-seq-2'},
    {'name': 'C', 'color': 'ylorrd-9-seq-3'},
    {'name': 'D', 'color': 'ylorrd-9-seq-4'},
    {'name': 'E', 'color': 'ylorrd-9-seq-5'},
    {'name': 'F', 'color': 'gnbu-9-seq-1'},
    {'name': 'G', 'color': 'gnbu-9-seq-2'},
    {'name': 'H', 'color': 'gnbu-9-seq-3'},
    {'name': 'I', 'color': 'gnbu-9-seq-4'},
    {'name': 'J', 'color': 'gnbu-9-seq-5'},
    {'name': 'K', 'color': 'gnbu-9-seq-6'},
    {'name': 'L', 'color': 'reds-9-seq-1'},
    {'name': 'M', 'color': 'reds-9-seq-2'},
    {'name': 'N', 'color': 'reds-9-seq-3'},
    {'name': 'V', 'color': 'reds-9-seq-4'},
    {'name': 'Z', 'color': 'reds-9-seq-5'},
    ]


data_path = "/home/rgarcia/caopsci/trending_topics/Data/circos"

for year in range(1988,2014):
    os.makedirs(str(year))

    shutil.copy('templates/bands.conf', str(year) )
    shutil.copy('templates/colors.conf', str(year) )
    shutil.copy('templates/ideogram.conf', str(year) )
    shutil.copy('templates/ideogram.label.conf', str(year) )
    shutil.copy('templates/ideogram.position.conf', str(year) )
    

    with open(str(year)+'/circos.conf', 'w') as f:
        f.write( circos_conf.render( citation_depth = data_path+'/citation_depth_'+str(year)+'.tsv',
                                     links          = data_path+'/branch_nx_l3_'+str(year)+'.links',
                                     contigs        = contigs ) )
